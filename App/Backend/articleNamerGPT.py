from langchain_openai import AzureChatOpenAI  # Adjust based on actual import paths
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import json
from dotenv import load_dotenv
import time

# Import the necessary LangChain components

def generateTitleWithLangChain(llm, output_parser,articles):
    load_dotenv()

    # Convert article list to a string format acceptable by our prompt
    dictToString = json.dumps({article['id']: article['name'] for article in articles})

    # Define the prompt template for topic choosing
    prompt_template = '''
        You are a topic chooser for a children's app. Given a list of article names and ids in JSON format, choose interesting articles that best represent an open topic that is diverse and suitable
        for a 7-12 year old age group. Do not add quizzes and videos. Replace the chosen article names with a 1-2 word representative topic name and replace the other names with '_'. 
        The topic name must be original (no duplicates) but also simple. Do not repeat names, make them unique.
        encapsulating the article's main subject (e.g. Space mission, New Bacteria, Killer Whale). Always return in the same JSON format as input (id: new name). Keep the formatting the same or else the system will not be able to read it.
        Article list: {articles}
    '''

    prompt = ChatPromptTemplate.from_template(prompt_template)
    input_variables = {"articles": dictToString}

    # Main Chain
    chain = prompt | llm | output_parser
    output = chain.invoke(input_variables)
    
    # Print and return the output
    print("Output: ", output)
    return output

def getArticles(dir):
    with open(dir, 'r') as file:
        articles = json.load(file)
    return articles

def addNewNames(nameDict, dir):
    articleDict = {}
    try:
        for id, new_name in nameDict.items():
            articleDict[int(id)] = new_name.strip()
    except ValueError as e:
        print("Error:", e)
        print("Reprompting GPT to resend the correct format...")
        time.sleep(2)
        generateNewNames()
        return

    with open(dir, 'r') as file:
        articles = json.load(file)
        
    updated_articles = []
    for article in articles:
        if article['id'] in articleDict:
            if articleDict[article['id']] != "_":
                article['new_title'] = articleDict[article['id']]
                updated_articles.append(article)
        else:
            updated_articles.append(article)

    with open(dir, 'w') as file:
        json.dump(updated_articles, file, indent=2)


def generateNewNames(llm, output_parser):
    dir = 'data/output.json'
    articles = getArticles(dir)
    newNames = generateTitleWithLangChain(llm, output_parser,articles)
    addNewNames(newNames, dir)
