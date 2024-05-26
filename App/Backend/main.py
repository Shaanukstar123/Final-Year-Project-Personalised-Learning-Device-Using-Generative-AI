from flask import Flask, jsonify, request, Response
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
import assemblyai as aai
from openai import OpenAI
from io import BytesIO

from google.oauth2 import service_account
from google.cloud import texttospeech

import re
import os
import json
import requests
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/GoogleFypKey.json"
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

#storyChain = initialiseModel()
'''ROUTES'''
storyChain = initialiseModel()

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
    dallePrompt = "2D cartoon child-friendly image of this description: " + prompt
    imageUrl = generateImageWithDALLE(dallePrompt)
    return jsonify({'imageUrl': imageUrl})

@app.route('/fetch_story/<id>', methods=['GET'])
def fetch_story(id):
    global storyChain
    imagePrompt = ""
    storyChain = initialiseModel()
    articleContent = getArticleContent(id)
    response = initialiseStory(articleContent, storyChain)
    # promptRegex = re.compile(r'dall-e prompt:\s*(.*)', re.IGNORECASE)
    # match = promptRegex.search(response)
    # if match:
    #     imagePrompt = match.group(1)
    #     print("match found: ", imagePrompt)
    # else:
    #     imagePrompt = summariseText(response)
    #     print("No match found: ",imagePrompt)
    print("response before cleanup: ", response)
    response, imagePrompt, question = cleanResponse(response)
    if imagePrompt == "":
        imagePrompt = summariseText(response)
        print("No match found: ",imagePrompt)
    print("text after cleanup: ", response)
    #response = cleanUpText(response)
    return jsonify({"story": response, "imagePrompt": imagePrompt, "question": question})
        
@app.route('/continue_story', methods=['GET'])
def continue_story():
    global storyChain
    user_input = request.args.get('user_input', '')
    print(f"Received user input: {user_input}")
    response = continueStory(storyChain, user_input)
    promptRegex = re.compile(r'dall-e prompt:\s*(.*)', re.IGNORECASE)
    match = promptRegex.search(response)
    if match:
        imagePrompt = match.group(1)
    else:
        imagePrompt = summariseText(response)
    
    return jsonify({"story": response, "imagePrompt": imagePrompt})


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
    
'''Helper Functions'''

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

def generateFirstPage(article, chain):
    # Generate story
    print("Generating story...")
    story = initialiseStory(article, chain)
    print(story)

    dallePrompt = generateImage(story)
    # Generate image
    fullDallePrompt= "2D cartoon child-friendly image with no text of this story: " + dallePrompt
    print("Generating image...")
    image_url = generateImageWithDALLE(fullDallePrompt)
    story = re.split(r"dall-e prompt:", story, flags=re.IGNORECASE)[0]
    return story, image_url

def generateNextPage(userOutput, chain):
    output = continueStory(chain, userOutput)
    dallePrompt = "2D cartoon child-friendly image with no text of this story: " + generateImage(output)
    image_url = generateImageWithDALLE(dallePrompt)
    output = output.split("DALL-E Prompt:")[0]
    return output, image_url

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
    app.run(debug=True)


