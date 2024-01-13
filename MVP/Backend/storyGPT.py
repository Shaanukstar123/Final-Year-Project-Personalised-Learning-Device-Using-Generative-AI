from openai import OpenAI
import json

client = OpenAI(api_key='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')

def generateStoryWithGPT(article):
    messages =[{"role": "system", "content": 
                "given an article, generate an interactive story based on the article for young children that explains the"
                 +"main concepts of the article without the actual details of the article. Mention a summary of the article at the top."
                },{"role": "user", "content": article}]
    chat = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
    reply = chat.choices[0].message.content
    return (reply)