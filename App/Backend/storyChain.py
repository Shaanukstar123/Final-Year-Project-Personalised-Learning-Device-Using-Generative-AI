from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationKGMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os
#import .env file
from dotenv import load_dotenv

#instantiate model so it can be passed between functions

def initialiseModel():
    load_dotenv()
    #get key from .env
    llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"), model = "gpt-3.5-turbo-0125")
    output_parser = StrOutputParser() #converts output to string
    memory = ConversationKGMemory(llm=llm)

    prompt_text = """
    You are telling a story based on a news article, tailored for children aged 5-10. Introduce the article first before starting the story.
    The story will evolve with user interaction as you ask them questions and change the story according to their answers, designed to engage the young reader and encourage critical thinking. 
    Each segment of the story concludes with 1 question that directs the narrative, followed by a DALL-E prompt for visualizing the story's current events.

    History: {history}
    Input: {input}
    """

    prompt = PromptTemplate(input_variables=["input"], template=prompt_text)
    #story chain with llm, prompt and memory with output parser as string
    storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory, output_parser=output_parser)
    #storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    return storyChain

def initialiseStory(article, storyChain):
    memory = storyChain.memory
    #save input article to memory
    memory.save_context({"input": "Article Summary"}, {"output": article})
    output = storyChain.predict(input=article)
    #save the output to memory
    memory.save_context({"input": "latest"}, {"output": output})
    return output

def continueStory(conversation_chain, user_input):
    memory = conversation_chain.memory
    
    # Load current story context from memory
    story_context = memory.load_memory_variables({"input": "latest"})
    
    # Assuming 'predict' or a similar function uses the current context and user input
    output = conversation_chain.predict(input=user_input, context=story_context)
    
    # Update memory with new story part, question, and DALL-E prompt
    memory.save_context({"input": user_input}, {"output": output["story"]})
    memory.save_context({"input": "Question"}, {"output": output["question"]})
    memory.save_context({"input": "DALL-E Prompt"}, {"output": output["dalle_prompt"]})
    
    return output
