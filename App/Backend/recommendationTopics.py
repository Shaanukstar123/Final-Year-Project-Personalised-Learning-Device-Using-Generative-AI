from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


def generateRecommendationTopics(llm, output_parser,recommendations):

    prompt_template = '''
        Given a list of words, be creative and make up a list of 20-50 specific story titles or quiz titles that are related to these words.
        Make them very specific and not generic E.g. "Space = The Moon Landing", "History = King Tut's Tomb"...
        Target age group is 7-12 years old.
        The return format must always be a JSON in the form "topics": ["title1", "title2", "title3"]. Make sure the title names are unique.
        Words: {recommendations}
    '''

    recommendations_str = ", ".join(recommendations)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    input_variables = {"recommendations": recommendations_str}

    # Main Chain
    chain = prompt | llm | output_parser
    output = chain.invoke(input_variables)
    
    # Print and return the output
    print("Generated Topics: ", output)
    return output
