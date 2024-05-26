from flask import Flask, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

def generateImageWithDALLE(prompt):
    #return "https://contenthub-static.grammarly.com/blog/wp-content/uploads/2020/10/Write-a-Story.jpg"
    response = client.images.generate(
        prompt=prompt,
        n=1,  # Number of images to generate
        size='256×256',  # Size of the image
        #dalle2
        model = 'image-dalle-2',
        
    )
    # Assuming the API returns a list of generated images
    imageUrl = response.data[0].url  # or however the URL is returned in the response
    
    return imageUrl
