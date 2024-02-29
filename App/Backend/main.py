from flask import Flask, jsonify
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import storyChain
from imageGenerator import generateImageWithDALLE
from textSummariser import summariseText
import concurrent.futures

import json

app = Flask(__name__)
CORS(app) 

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
    

def getArticleContent(id):
    with open('data/output.json', 'r') as file:
        data = json.load(file)
        for article in data:
            if int(article['id']) == int(id):
                return article['content']
    return None
    
def generateStoryAndImage(article):
    # Generate story
    print("Generating story...")
    story = storyChain(article)
    dallePrompt = ""
    print(story)

    if "DALLE:" in story:
        summary = story.split("DALLE:")[1]
        print("DALLE prompt found:")
        dallePrompt = article
        
    else:
        print("No DALLE prompt")
        dallePrompt = summariseText(article)

    # Generate image
    fullDallePrompt= "2D cartoon child-friendly image with no text of this story: " + dallePrompt
    print("Generating image...")
    image_url = generateImageWithDALLE(fullDallePrompt)
    return story, image_url
    
@app.route('/fetch_story/<id>', methods=['GET'])
def get_story(id):
        articleContent = getArticleContent(id)
        if articleContent:
            story, image_url = generateStoryAndImage(articleContent)
            return jsonify({"story": story, "image_url": image_url})
        else:
            return jsonify({"error": "Article not found"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)
