from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
#import .env file
from dotenv import load_dotenv

def storyChain(article):
    load_dotenv()
    #get key from .env
    llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"), model = "gpt-3.5-turbo-0125")
    output_parser = StrOutputParser() #converts output to string

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a young children's (age 5-10) storyteller that takes an input article and creates an educational story out of it."
        +"For every prompt you: Introduce a summary of the article and what has happened in the first paragraph to a 6 year old kid." 
        +"Then generate a creative story of 5-8 paragraphs based on the article which explains the main"
        +"topic of the article which will be given. "),
        ("user", "{input}")
    ])

    #Main Chain
    chain = prompt | llm | output_parser

    output = chain.invoke({"input": article})
    return output

