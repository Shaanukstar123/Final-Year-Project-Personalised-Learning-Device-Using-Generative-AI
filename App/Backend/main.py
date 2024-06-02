from flask import Flask, jsonify, request, Response
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from generateContent import initialiseContentModel, initialiseContent, continueContent
from subjectChain import generateSubjectTopics
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
from database import initialiseDatabase
from clustering import run_clustering_on_db
import assemblyai as aai
from openai import OpenAI
from io import BytesIO

from google.oauth2 import service_account
from google.cloud import texttospeech

import re
import os
import json
import requests
import sqlite3
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
    response, imagePrompt, question = cleanResponse(response)
    if imagePrompt == "":
        imagePrompt = summariseText(response)
    store_story(id, response, imagePrompt, "", question)
    return jsonify({"story": response, "imagePrompt": imagePrompt, "question": question})

@app.route('/fetch_content', methods=['GET'])
def fetch_content():
    topic = request.args.get('topic', '')
    global contentChain
    contentChain = initialiseContentModel()
    response = initialiseContent(contentChain, topic)
    response, imagePrompt, question = cleanResponse(response)
    store_story(topic, response, imagePrompt, "", question)
    return jsonify({"story": response, "imagePrompt": imagePrompt, "question": question})

@app.route('/continue_story', methods=['GET'])
def continue_story():
    global storyChain
    user_input = request.args.get('user_input', '')
    response = continueStory(storyChain, user_input)
    promptRegex = re.compile(r'dall-e prompt:\s*(.*)', re.IGNORECASE)
    match = promptRegex.search(response)
    if match:
        imagePrompt = match.group(1)
    else:
        imagePrompt = summariseText(response)
    append_story(user_input, response, imagePrompt)
    return jsonify({"story": response, "imagePrompt": imagePrompt})

@app.route('/continue_content', methods=['GET'])
def continue_content():
    global contentChain
    user_input = request.args.get('user_input', '')
    response = continueContent(contentChain, user_input)
    promptRegex = re.compile(r'dall-e prompt:\s*(.*)', re.IGNORECASE)
    match = promptRegex.search(response)
    if match:
        imagePrompt = match.group(1)
    else:
        imagePrompt = summariseText(response)
    append_story(user_input, response, imagePrompt)
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

    
    # Fetch topics related to the subject from your data source
    # try:
    #     with open('data/output.json', 'r') as file:
    #         data = json.load(file)
    #         subject_topics = [article for article in data if article['subject'].lower() == subject.lower()]
    #         return jsonify(subject_topics)
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

def store_story(topic_id, story, image_prompt, image_url, question):
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stories (topic_id, story, image_prompt, image_url, question)
        VALUES (?, ?, ?, ?, ?)
    ''', (topic_id, story, image_prompt, image_url, question))
    conn.commit()
    conn.close()

def append_story(topic_id, story, image_prompt):
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT story FROM stories WHERE topic_id = ?
    ''', (topic_id,))
    result = cursor.fetchone()
    if result:
        current_story = result[0] + ' ' + story
        cursor.execute('''
            UPDATE stories
            SET story = ?, image_prompt = ?
            WHERE topic_id = ?
        ''', (current_story, image_prompt, topic_id))
        conn.commit()
    conn.close()

def clear_database():
    conn = sqlite3.connect('data/stories.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stories')
    conn.commit()
    conn.close()


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
    # Convert text to lower case for consistent searching
    text_lower = text.lower()

    # Find start and end indices for each section
    dalle_prompt_start = text_lower.find('dall-e prompt:')
    story_start = text_lower.find('story:')
    question_start = text_lower.find('question:')

    if dalle_prompt_start == -1 or story_start == -1 or question_start == -1:
        return "", "", text.strip()

    # Extract DALL-E Prompt
    dalle_prompt = text[dalle_prompt_start + len('dall-e prompt:'):story_start].strip()

    # Extract Question
    question = text[question_start + len('question:'):].strip()

    # Extract STORY content
    story_content = text[story_start + len('story:'):question_start].strip()

    # Remove other words with colons from STORY content
    cleaned_response = re.sub(r'\b\w+:\s*', '', story_content)

    return cleaned_response.strip(), dalle_prompt, question 
    
    
if __name__ == "__main__":
    initialiseDatabase()
    app.run(debug=True)


