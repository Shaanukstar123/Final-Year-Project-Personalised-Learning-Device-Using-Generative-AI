from flask import Flask, jsonify
from flask_cors import CORS
# from threading import Thread
from webCrawler.newsGrabber import run_crawler
from articleNamerGPT import generateNewNames
from storyChain import storyChain
from imageGenerator import generateImageWithDALLE
from textSummariser import summarise_text

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
    
@app.route('/fetch_story/<id>', methods=['GET'])
def get_story(id):
    with open('data/output.json', 'r') as file:
        data = json.load(file)
        for article in data:
            if int(article['id']) == int(id):
                print(int(article['id']))
                print("Generating Story")
                story = storyChain(article['content'])
                print("start summary")
                summarised_story = summarise_text(story)
                print("summarised")
                image_url = generateImageWithDALLE("2D cartoon child-friendly image of this story: " + summarised_story)
                return jsonify({"story": story, "image_url": image_url})
        return ("Article not found")
    
if __name__ == "__main__":
    app.run(debug=True)
