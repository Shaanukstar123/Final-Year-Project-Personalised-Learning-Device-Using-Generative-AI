from flask import Flask, jsonify
from openai import OpenAI
import json

app = Flask(__name__)
client = OpenAI(api_key='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')

def generateImageWithDALLE(prompt):
    response = client.images.generate(
        prompt=prompt,
        n=1,  # Number of images to generate
        size="512x512"  # Size of the image
    )
    # Assuming the API returns a list of generated images
    image_url = response.data[0].url  # or however the URL is returned in the response
    return image_url
