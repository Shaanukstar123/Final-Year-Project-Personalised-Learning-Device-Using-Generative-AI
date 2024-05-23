from flask import Flask, jsonify, request, Response
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
import assemblyai as aai

import re
import os
import json
import requests
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app) 

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
    text_content = request.json.get('text', '')
    # Assume generateImage returns a URL to an image or saves the image and returns its path
    dallePrompt = "2D cartoon child-friendly image with no text of this story: " + generateImage(text_content)
    image_url = generateImageWithDALLE(dallePrompt)
    return jsonify({'image_url': image_url})

@app.route('/fetch_story/<id>', methods=['GET'])
def fetch_story(id):
    global storyChain
    storyChain = initialiseModel()
    articleContent = getArticleContent(id)
    response = initialiseStory(articleContent, storyChain)
    return jsonify({"story": response})
    # if articleContent:
    #     return Response(stream_story(articleContent, storyChain),
    #                     mimetype="text/event-stream")
    # else:
    #     return jsonify({"error": "Article not found"}), 404
    
    
# def stream_story(articleContent, storyChain):
#     story_gen = initialiseStory(articleContent, storyChain)
#     print("Type of story Gen: ",type(story_gen))
#     try:
#         for story_part in story_gen:
#             yield f"data: {story_part}\n\n"
#     except GeneratorExit:
#         print("Stream closed")
        
@app.route('/continue_story', methods=['GET'])
def continue_story():
    global storyChain
    user_input = request.args.get('user_input', '')
    print(f"Received user input: {user_input}")
    response = continueStory(storyChain, user_input)
    return jsonify({"story": response})
#     return Response(continue_story_stream(user_input, storyChain),
#                     mimetype="text/event-stream")

# def continue_story_stream(user_input, storyChain):
#     print("Starting story continuation stream...")
#     story_continuation_gen = continueStory(storyChain, user_input)
#     try:
#         for story_part in story_continuation_gen:
#             # print(f"Streaming story part: {story_part}")
#             yield f"data: {story_part}\n\n"
#     except GeneratorExit:
#         print("Stream closed")

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
    return jsonify({"message": "Audio file generated"}), 200
    ##TEST^^^###
    voice_id = "onwK4e9ZLuTAKqWW03F9"  # Example: British Daniel
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
    }
    data = request.json
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content, response.status_code, {'Content-Type': 'audio/mpeg'}
    else:
        return jsonify({"error": "Failed to generate speech"}), response.status_code

    ##Return the audio file instead 
    
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

    
    
if __name__ == "__main__":
    app.run(debug=True)


