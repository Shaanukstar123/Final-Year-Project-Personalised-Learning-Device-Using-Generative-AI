from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

def initialiseAzureModel():
    llm = AzureChatOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )
    output_parser = JsonOutputParser()  # Converts output to JSON
    return llm, output_parser

def generateSubjectTopics(subject):
    llm, output_parser = initialiseAzureModel()

    prompt_template = '''
        Given a school subject, you must return a list of 30-50 interesting topic titles related to that subject. For context, the titles will be used
        to make stories, riddles, and quizzes for 7-12 year olds. It must be be 1-5 words and should be unique and educational. E.g. Subject = "Science". 
        Titles = "Discovery of The Atom", "Is Pluto a Planet?", "Evolution", "Riddle me This".
        Maths = "Pythagoras", "What number am I?" "What's next in the Sequence?". Focus on names that make interesting stories, but for technical subjects like Maths, focus more on problems and riddles.
        The return format must always be a JSON in the form "topics": ["title1", "title2", "title3"].
        Subject: {subject}
    '''

    prompt = ChatPromptTemplate.from_template(prompt_template)
    input_variables = {"subject": subject}

    # Main Chain
    chain = prompt | llm | output_parser
    output = chain.invoke(input_variables)
    
    # Print and return the output
    print("Subject Titles: ", output)
    return output

