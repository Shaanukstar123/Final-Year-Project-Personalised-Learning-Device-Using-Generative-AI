from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationKGMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import os
import re 
import time
#import .env file
from dotenv import load_dotenv

#instantiate model so it can be passed between functions

def initialiseContentModel():
    load_dotenv()
    
    llm = AzureChatOpenAI(
        api_version = os.getenv("OPENAI_API_VERSION"), 
        api_key = os.getenv("AZURE_API_KEY"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )

    #llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"), model = "gpt-3.5-turbo-0125")
    output_parser = StrOutputParser() #converts output to string
    memory = ConversationBufferWindowMemory(k=4, ai_prefix="Teacher")#ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = """
    This is a conversation between a child and a teacher. You are the teacher. The child will provide a topic. Depending on the topic,
    you will provide educational entertainment directly talking to the child age 7-12. This can be in any form such as explaining a topic in detail, using stories, riddles, quizzes, 
    or a mode best suits the topic. The goal is to educate and entertain the child
    on the topic. Do no deviate too far from the topic. If asking questions, limit it to a single one and wait for a response.
    If images are needed, provide only a single Dall-E image prompt starting with "DALL-E Prompt:" at the beginning of the response.
    Always output the educational topics and genres that summarise the response starting with  "Themes: "

    Respond directly to the child in the first person as if you are talking to them.

    Current conversation: {history}
    Child: {input}
    Teacher: 
    """

    prompt = PromptTemplate(input_variables=["history", "input"], template=promptText)
    #story chain with llm, prompt and memory with output parser as string
    storyChain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        output_parser=output_parser,
        verbose=True
    )
    #storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    print("Model initialised")
    return storyChain


# def streamStoryOutput(llm, prompt):
#     for output in llm.stream(prompt):
#         yield output 
        
def initialiseContent(contentChain, topic):
    #clear the memory
    #storyChain.memory.clear()
    # buffered_output = ""
    # for output in streamStoryOutput(storyChain.llm, article):
    #     buffered_output += output.content
    #     while True:
    #         match = re.search(r'\s', buffered_output)
    #         if not match:
    #             break
    #         index = match.start()
    #         yield buffered_output[:index + 1]
    #         buffered_output = buffered_output[index + 1:]

    # if buffered_output:
    #     yield buffered_output

    response = contentChain(topic)
    return response["response"]

def continueContent(contentChain, userInput):
    # print("Continuing story...")
    # buffered_output = ""
    # for output in streamStoryOutput(storyChain.llm, userInput):
    #     buffered_output += output
    #     while True:
    #         match = re.search(r'\s', buffered_output)
    #         if not match:
    #             break
    #         index = match.start()
    #         yield buffered_output[:index + 1]
    #         buffered_output = buffered_output[index + 1:]

    # if buffered_output:
    #     yield buffered_output
    response = contentChain(userInput)
    print(response["response"])
    return response["response"]

