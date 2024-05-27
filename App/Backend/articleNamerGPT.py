from langchain_openai import AzureChatOpenAI  # Adjust based on actual import paths
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import json
from dotenv import load_dotenv
import time

# Import the necessary LangChain components

def initialiseAzureModel():
    load_dotenv()
    llm = AzureChatOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )
    output_parser = JsonOutputParser()  # Converts output to JSON
    return llm, output_parser

def generateTitleWithLangChain(articles):
    load_dotenv()

    llm, output_parser = initialiseAzureModel()

    # Convert article list to a string format acceptable by our prompt
    dictToString = json.dumps({article['id']: article['name'] for article in articles})

    # Define the prompt template for topic choosing
    prompt_template = '''
        You are a topic chooser for a children's app. Given a list of article names and ids in JSON format, choose only the most interesting articles that best represent an open topic that is diverse and suitable
        for a 7-12 year old age group. These are webscraped articles so ignore quizzes and videos. Replace the chosen article names with the representative topic name and replace the other names with '_'. 
        The topic name must be original (no duplicates) but also simple (one or two words) and
        encapsulating the article's main subject (e.g. Space mission, New Bacteria, Killer Whale). Always return in the same JSON format as input (id: new name). Keep the formatting the same or else the system will not be able to read it.
        Here is the list: {articles}
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


def generateNewNames():
    dir = 'data/output.json'
    articles = getArticles(dir)
    newNames = generateTitleWithLangChain(articles)
    addNewNames(newNames, dir)
