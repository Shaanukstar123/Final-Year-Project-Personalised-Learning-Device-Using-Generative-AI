from flask import Flask, jsonify
from openai import OpenAI
import os

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

def generateImageWithDALLE(prompt):
    response = client.images.generate(
        prompt=prompt,
        n=1,  # Number of images to generate
        size="1024x1024",  # Size of the image
        model = "dall-e-3"
    )
    # Assuming the API returns a list of generated images
    image_url = response.data[0].url  # or however the URL is returned in the response
    return image_url
