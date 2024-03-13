from flask import Flask, jsonify
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
from flask import request
import re
import os
import json
import requests


app = Flask(__name__)
CORS(app) 

storyChain = initialiseModel()
'''ROUTES'''

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
    

@app.route('/fetch_story/<id>', methods=['GET'])
def get_story(id):
        articleContent = getArticleContent(id)
        if articleContent:
            story, image_url = generateFirstPage(articleContent,storyChain)
            return jsonify({"story": story, "image_url": image_url})
            #return jsonify({"story": "Hello hello testing testing", "image_url": "https://contenthub-static.grammarly.com/blog/wp-content/uploads/2020/10/Write-a-Story.jpg"})
        else:
            return jsonify({"error": "Article not found"}), 404
        
        
@app.route('/continue_story/', methods=['POST'])
def continue_story():
    # Extract user input from the request
    user_input = request.json.get('user_input', '')
    user_input = str(user_input)
    # Continue the story
    output, imageUrl = generateNextPage(user_input, storyChain)
    #return jsonify({"story": "hello hello testing 2 testing 2", "image_url": "https://contenthub-static.grammarly.com/blog/wp-content/uploads/2020/10/Write-a-Story.jpg"})
    return jsonify({"story": output, "image_url": imageUrl})

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
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


