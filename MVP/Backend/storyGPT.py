from openai import OpenAI
import json
import os
from dotenv import load_dotenv

#load dotenv
load_dotenv()

client = OpenAI(os.getenv("OPENAI_API_KEY"))

def generateStoryWithGPT(article):
    messages =[{"role": "user", "content": article}, {"role": "system", "content": 
                "Introduce a summary of the article and what has happened in the first paragraph to a 6 year old kid. Then generate a creative story of 5-8 paragraphs based on the article which explains the main"
                 +"topic of the article which will be given."
                }]
    chat = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages
        )
    reply = chat.choices[0].message.content
    return (reply)