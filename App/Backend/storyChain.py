from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationKGMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
import os
#import .env file
from dotenv import load_dotenv

#instantiate model so it can be passed between functions

def initialiseModel():
    load_dotenv()
    
    llm = AzureChatOpenAI(
        api_version = os.getenv("OPENAI_API_VERSION"), 
        api_key = os.getenv("AZURE_API_KEY"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )

    #llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"), model = "gpt-3.5-turbo-0125")
    output_parser = StrOutputParser() #converts output to string
    memory = ConversationSummaryBufferMemory(llm=llm)
    promptText = """
    The following is a continuous interactive educational children's story-telling session based on the topic of a given news article. Generate a page that will continue the story after each
    prompt input. User input will determine how the story changes in the current page. Continue the story given the history of chat by the conversational summary buffer memory. Ask an educational question 
    at the end of the page that relates to the story
    and can change the direction of the narrative. 
    The article will be introduced first before starting the story.
    Each segment (page) of the story concludes with 1 question that starts with "Question: ", which directs the narrative, followed by a DALL-E prompt for visualizing the story's current events beginning with "DALL-E Prompt:".

    History of chat: {history}
    User input to the previous question: {input}
    """

    prompt = PromptTemplate(input_variables=["history", "input"], output_variables=["output"], template=promptText)
    #story chain with llm, prompt and memory with output parser as string
    storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory, output_parser=output_parser, verbose=True)
    #storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    return storyChain

def saveToMemory(memory, new_content):
    # Retrieve existing story history from memory
    existingHistory = memory.load_memory_variables({"input": "history"})
    updatedHistory = existingHistory.get("history", "") + " " + new_content
    
    # Now save the updated history back into memory
    memory.save_context({"input": "history"}, {"output": updatedHistory})
    print

def initialiseStory(article, storyChain):
    memory = storyChain.memory
    initialContext = "First introduce this news article and then begin the educational story about the subject of the article. Article Summary: " + article
    #saveToMemory(memory, initialContext)
    output = storyChain.predict(input=initialContext)
    #save the output to memory
    #saveToMemory(memory, output)
    print("Memory: ",memory)
    #memory.save_context({"input": "latest"}, {"output": output})
    return output

def continueStory(storyChain, userInput):
    memory = storyChain.memory
    # Load current story context from memory
    #storyContext = memory.load_memory_variables({})
    # print("Cumulative story context: ",storyContext)
    # cumulativeInput = ""
    # if storyContext.get("history"):
    #     cumulativeInput = f"{storyContext['history']} {userInput}"
    # else:
    #     cumulativeInput = userInput
    # Assuming 'predict' or a similar function uses the current context and user input
    # output = storyChain.predict(input=cumulativeInput)
    prompt = '''This is the user output to the question asked in the previous page of the story (stored in conversatinal buffer memory). Continue the story based on the user's answer with a new page and question at the
    end, or conclude the story if necessary by ending with "THE END". User's answer to previous question:''' + userInput
    output = storyChain.predict(input=prompt)
    print("Output: ",output)
    #saveToMemory(memory, output)
    print("MemoryContinued: ",memory)
    return output
