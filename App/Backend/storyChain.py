from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationKGMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
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
    memory = ConversationKGMemory(llm=llm)

    promptText = """
    The following is an interactive educational children's story-telling session based on the topic of a given news article. The story is tailored for children aged 5-10. The article will be introduced first before starting the story.
    The story will evolve with user interaction as you ask them questions and change the story according to their answers, designed to engage the young reader and encourage critical thinking. 
    Only one page of the story will be generated each time and history of the context will be tracked.
    Each segment (page) of the story concludes with 1 question that directs the narrative, followed by a DALL-E prompt for visualizing the story's current events beginning with "DALL-E Prompt:".

    Chat History: {history}
    Input: {input}
    Storyteller: 
    """

    prompt = PromptTemplate(input_variables=["history", "input"], output_variables=["output"], template=promptText)
    #story chain with llm, prompt and memory with output parser as string
    storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory, output_parser=output_parser)
    #storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    return storyChain

def saveToMemory(memory, new_content):
    # Retrieve existing story history from memory
    existingHistory = memory.load_memory_variables({"input": "history"})
    updatedHistory = existingHistory.get("history", "") + " " + new_content
    
    # Now save the updated history back into memory
    memory.save_context({"input": "history"}, {"output": updatedHistory})

def initialiseStory(article, storyChain):
    memory = storyChain.memory
    initialContext = "Article Summary: " + article 
    memory.save_context({"input": "initial"}, {"output": initialContext})
    output = storyChain.predict(input=initialContext)
    #save the output to memory
    memory.save_context({"input": "initial"}, {"output": output})
    #memory.save_context({"input": "latest"}, {"output": output})
    return output

def continueStory(storyChain, userInput):
    memory = storyChain.memory
    # Load current story context from memory
    storyContext = memory.load_memory_variables({"input": "history"})
    print("Cumulative story context: ",storyContext)
    
    if storyContext.get("history"):
        cumulativeInput = f"{storyContext['history']} {userInput}"
    else:
        cumulativeInput = userInput
    # Assuming 'predict' or a similar function uses the current context and user input
    output = storyChain.predict(input=userInput)
    saveToMemory(memory, output)
    return output
