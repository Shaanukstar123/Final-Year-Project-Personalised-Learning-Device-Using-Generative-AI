from flask import Flask, jsonify
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import initialiseStory, initialiseModel, continueStory
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
import concurrent.futures
from flask import request

import json

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
        else:
            return jsonify({"error": "Article not found"}), 404
        
        
@app.route('/continue_story/<id>', methods=['POST'])
def continue_story(id):
    # Extract user input from the request
    user_input = request.json.get('user_input', '')
    # Continue the story
    output, imageUrl = generateNextPage(user_input, storyChain)
    return jsonify({"story": output, "image_url": imageUrl})



'''Helper Functions'''

def getArticleContent(id):
    with open('data/output.json', 'r') as file:
        data = json.load(file)
        for article in data:
            if int(article['id']) == int(id):
                return article['content']
    return None

    
def generateImage(text):
    if "DALL-E Prompt:" in text:
        summary = text.split("DALL-E Prompt:")[1]
        print("DALLE prompt found:", summary)
        return summary
        
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
    story = story.split("DALL-E Prompt:")[0]
    return story, image_url

def generateNextPage(userOutput, chain):
    output = continueStory(chain, userOutput)
    dallePrompt = "2D cartoon child-friendly image with no text of this story: " + generateImage(output)
    image_url = generateImageWithDALLE(dallePrompt)
    output = output.split("DALL-E Prompt:")[0]
    return output, image_url

    
    
if __name__ == "__main__":
    app.run(debug=True)


