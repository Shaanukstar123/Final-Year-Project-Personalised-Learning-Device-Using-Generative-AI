from flask import Flask, jsonify
from openai import OpenAI
import os

client = OpenAI(api_key="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")

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
