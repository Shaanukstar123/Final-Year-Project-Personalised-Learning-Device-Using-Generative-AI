import re
import os
import json
import requests
import sqlite3

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from threading import Thread

from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from generateContent import initialiseContentModel, initialiseContent, continueContent
from subjectChain import generateSubjectTopics
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
from database import initialiseDatabase
from clustering import run_clustering_on_db
from topicColours import get_colour_for_topic

from recommendationTopics import generateRecommendationTopics
#from tests.apiTests import test_recommendation_topics

import assemblyai as aai
from openai import OpenAI
from io import BytesIO

from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/GoogleFypKey.json"
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

#storyChain = initialiseModel()
'''ROUTES'''
storyChain = initialiseModel()
contentChain = initialiseContentModel()


@app.route('/update_news', methods=['GET'])
def start_crawler():
    run_crawler()
    return ("data fetched")

@app.route('/get_topics', methods=['GET'])
def get_topics():
    generateNewNames() #updates json with new topic names
    with open('data/output.json', 'r') as file:
        data = json.load(file)
        return jsonify(data)
    
@app.route('/get_image', methods=['POST'])
def get_image():
    prompt = request.json.get('text', '')
    # Assume generateImage returns a URL to an image or saves the image and returns its path
    dallePrompt = "2D cartoon child-friendly image of this description: " + prompt + " No text."
    imageUrl = generateImageWithDALLE(dallePrompt)
    return jsonify({'imageUrl': imageUrl})

@app.route('/fetch_story/<id>', methods=['GET'])
def fetch_story(id):
    global storyChain
    imagePrompt = ""
    storyChain = initialiseModel()
    articleContent = getArticleContent(id)
    response = initialiseStory(articleContent, storyChain)
    print("Response: ", response)
    response, imagePrompt, question, themes = cleanResponse(response)
    store_story(id, response, imagePrompt, "", question, themes)
    check_and_run_clustering()
    return jsonify({"story": response, "imagePrompt": imagePrompt, "question": question})

@app.route('/fetch_content', methods=['GET'])
def fetch_content():
    topic = request.args.get('topic', '')
    global contentChain
    contentChain = initialiseContentModel()
    response = initialiseContent(contentChain, topic)
    print("Response: ", response)
    response, imagePrompt, question, themes = cleanResponse(response)
    store_story(topic, response, imagePrompt, "", question, themes)
    check_and_run_clustering()
    return jsonify({"story": response, "imagePrompt": imagePrompt, "question": question})


@app.route('/continue_story', methods=['GET'])
def continue_story():
    global storyChain
    user_input = request.args.get('user_input', '')
    response = continueStory(storyChain, user_input)
    print("Response: ", response)
    response, imagePrompt, question, themes = cleanResponse(response)
    response = response + question
    append_story(user_input, (response), imagePrompt, themes)
    return jsonify({"story": response, "imagePrompt": imagePrompt})

@app.route('/continue_content', methods=['GET'])
def continue_content():
    global contentChain
    user_input = request.args.get('user_input', '')
    response = continueContent(contentChain, user_input)
    response, imagePrompt, question, themes = cleanResponse(response)
    append_story(user_input, response, imagePrompt, themes)
    return jsonify({"story": response, "imagePrompt": imagePrompt})

@app.route('/get_subject_topics', methods=['GET'])
def get_subject_topics():
    subject = request.args.get('subject', '')
    #subjects = ['history', 'geography', 'maths', 'science', 'english', 'music']
    if not subject:
        return jsonify({'error': 'Subject is required'}), 400
    return generateSubjectTopics(subject)
    try:
        return get_subject_topics(subject)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendation_topics', methods=['GET'])
def recommendation_topics():
    recommendations = get_recommendations_from_db()  # Your existing function to get recommendations
    topics_with_colors = []

    for topic in recommendations:
        color = get_colour_for_topic(topic)
        topics_with_colors.append({"topic": topic, "color": color})
    print("Topics with colors: ", topics_with_colors)

    return jsonify({"topics": topics_with_colors})
    # try:
        
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


#Speech to text api token fetcher
@app.route('/get_token', methods=['GET'])
def get_token():
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    headers = {
        'authorization': api_key
    }
    data = {
        'expires_in': 3600  # Token valid for 1 hour
    }
    response = requests.post(
        'https://api.assemblyai.com/v2/realtime/token',
        headers=headers,
        json=data  # Ensure to send data as JSON
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to generate token', 'details': response.text}), response.status_code

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    client = OpenAI()
    data = request.json
    text = data.get("text", "")

    try:
        # Generate speech using OpenAI's TTS
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=text
        )

        # # Create an in-memory bytes buffer to hold the audio content
        # audio_content = BytesIO(response.audio_content)
        # audio_content.seek(0)  # Rewind the buffer to the beginning
        audio_content = BytesIO()
            
            # Stream the response content into the buffer
        for chunk in response.iter_bytes():
            audio_content.write(chunk)
            
        audio_content.seek(0)  # Rewind the buffer to the beginning
        print("Audio content generated successfully")
        return Response(audio_content.read(), mimetype='audio/mpeg')

    except Exception as e:
        print(f"Failed to generate speech: {e}")
        return jsonify({"error": "Failed to generate speech"}), 500
    
@app.route('/clear_database', methods=['POST'])
def clear_db():
    try:
        clear_database()
        return jsonify({"message": "Database cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/run_clustering', methods=['GET'])
def run_clustering():
    try:
        run_clustering_on_db()
        return jsonify({"message": "Clustering run successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
'''Helper Functions'''

def store_story(topic_id, story, image_prompt, image_url, question, themes):
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stories (topic_id, story, image_prompt, image_url, question, themes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (topic_id, story, image_prompt, image_url, question, themes))
    conn.commit()
    conn.close()

def append_story(topic_id, story, image_prompt, new_themes):
    if new_themes:
        new_themes = ", " + new_themes
    else:
        new_themes = ""
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    
    # Fetch the current story and themes
    cursor.execute('''
        SELECT story, themes FROM stories WHERE topic_id = ?
    ''', (topic_id,))
    result = cursor.fetchone()
    
    if result:
        current_story = result[0] + ' ' + story
        current_themes = result[1] if result[1] else ''  # Handle case where themes might be NULL
        updated_themes = current_themes + ' ' + new_themes if current_themes else new_themes
        
        cursor.execute('''
            UPDATE stories
            SET story = ?, image_prompt = ?, themes = ?
            WHERE topic_id = ?
        ''', (current_story, image_prompt, updated_themes, topic_id))
        conn.commit()
    
    conn.close()

def clear_database():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stories')
    conn.commit()
    conn.close()

def get_recommendations_from_db():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('SELECT recommendations FROM recommendations')
    result = cursor.fetchone()
    conn.close()
    if result:
        recommendations = json.loads(result[0])
        return recommendations
    return []


def getArticleContent(id):
    with open('data/output.json', 'r') as file:
        data = json.load(file)
        for article in data:
            if int(article['id']) == int(id):
                return article['content']
    return None

    
def generateImage(text):
    # Check if DALLE prompt is already in the text regardless of case sensitivity in any part of the string
    if re.search(r"dall-e prompt:", text, flags=re.IGNORECASE):
        print("DALLE prompt already exists in text")
        return re.split(r"dall-e prompt:", text, flags=re.IGNORECASE)[1]
    
    print("No DALLE prompt")
    dallePrompt = summariseText(text)
    return dallePrompt

def cleanResponse(text):
    dallePrompt = ""
    cleanedResponse = text
    questionPrompt = ""
    themes = ""
    dalleMatch = re.search(r'DALL-E prompt:\s*(.*?)(\.|\n|$)', text, re.IGNORECASE)
    if dalleMatch:
        dallePrompt = dalleMatch.group(1).strip()
        # Remove the DALL-E prompt sentence from the text
        cleanedResponse = re.sub(re.escape(dalleMatch.group(0)), '', text, flags=re.IGNORECASE)
    themeMatch= re.search(r'Themes:\s*(.*?)(\.|\n|$)', text, re.IGNORECASE)
    if themeMatch:
        themes = themeMatch.group(1).strip()
        # Remove the DALL-E prompt sentence from the text
        cleanedResponse = re.sub(re.escape(themeMatch.group(0)), '', cleanedResponse, flags=re.IGNORECASE)
    # cleanedResponse = re.sub(r'DALL-E Prompt:\s*', '', text, re.IGNORECASE)
    questionMatch = re.search(r'question:\s*(.*)', text, re.IGNORECASE)
    if questionMatch:
        questionPrompt = questionMatch.group(1)

    return cleanedResponse, dallePrompt, questionPrompt, themes
    
def run_clustering_in_background():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM stories')
    count = cursor.fetchone()[0]
    if count % 1 == 0:
        run_clustering_on_db()
    conn.close()

def check_and_run_clustering():
    # Run the clustering function on a separate thread
    clustering_thread = Thread(target=run_clustering_in_background)
    clustering_thread.start()
    

def test_recommendation_topics():
    with app.test_client() as client:
        response = client.get('/recommendation_topics')
        print('Status Code:', response.status_code)

# test_recommendation_topics()
if __name__ == "__main__":
    initialiseDatabase()
    app.run(debug=True)



