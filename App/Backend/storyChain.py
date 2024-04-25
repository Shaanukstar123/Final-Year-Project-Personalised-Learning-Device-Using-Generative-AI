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
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = """
    The following is a continuous interactive educational children's story-telling session based on the topic of a given news article. Generate around 50 word page that will continue the story after each
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
    print("Model initialised")
    return storyChain

def saveToMemory(memory, new_content):
    # Retrieve existing story history from memory
    existingHistory = memory.load_memory_variables({"input": "history"})
    updatedHistory = existingHistory.get("history", "") + " " + new_content
    
    # Now save the updated history back into memory
    memory.save_context({"input": "history"}, {"output": updatedHistory})
    print

def streamStoryOutput(llm, prompt):
    for output in llm.stream(prompt):
        yield output 


def initialiseStory(article, storyChain):
    #clear memory
    storyChain.memory.clear()
    print("Initialising story")
    memory = storyChain.memory
    initialContext = "First introduce this news article and then begin the educational story about the subject of the article. Article Summary: " + article
    print("Initialised Context")
    for output in streamStoryOutput(storyChain.llm, initialContext):
        # print("Memory: ",memory)
        # print("TempOutput: ",output)
        yield output
    #saveToMemory(memory, initialContext)
    #output = storyChain.predict(input=initialContext)
    #save the output to memory
    #saveToMemory(memory, output)
    
    #memory.save_context({"input": "latest"}, {"output": output})
    #return output

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


if __name__ == "__main__":
    print ("Initialising model")
    storyChain = initialiseModel()
    article = "The un-manned space craft, named Peregrine, had a problem pointing its solar panels at the Sun to generate power. In trying to fix the issue the craft has lost \"critical\" amounts of fuel and time is running out to salvage anything from the mission, its engineers said. This video can not be played Watch: Vulcan rocket lifts off to the Moon Before encountering the fault, Peregrine launched successfully onboard a Vulcan rocket, that blasted off from Florida in the United States on Monday.  The lander is operated by private space company Astrobotic Technology. American space agency Nasa had paid for five pieces of scientific equipment to be carried onboard for experiments on the lunar surface. A successful landing, scheduled for 23 February, would have marked the  first time a private company had landed on the Moon's surface and would have been the first American made spacecraft on the surface of the Moon since the   17 mission in 1972. But that's no longer possible now and Astrobotic says it might not be able to control its spacecraft for much longer. Peregrine's problems were identified soon after communications had been established following its separation from the top of the Vulcan rocket.  Engineers noticed the spacecraft was struggling to maintain a stable lock on the Sun, meaning its solar cells were not receiving a constant supply of sunshine to recharge the onboard battery. Astrobotic's engineers eventually identified the cause as a failure in the propulsion system, and although they were able to successfully re-point the spacecraft and charge the battery, it was evident, the company said, that Peregrine had lost a significant amount of fuel in the process. As a result Astrobotic said it was reassessing its mission goals, which means looking at what could still be achievable in the circumstances. \"At this time the goal is to get Peregrine as close to lunar distance as we can before it loses the ability to maintain its Sun-pointing position and subsequently loses power,\" it said. Peregrine is just one of several spacecraft attempting to land on the lunar surface in 2024. As many as eight different projects, including those from Japan and China, could land on the Moon this year. Nasa is also offering members of the public the chance to have their name in space as part of its   in late 2024. The Viper, Nasa's first robotic moon rover, will journey on a mission to unexplored parts of the Moon's south pole. Nasa's   II mission is also scheduled for later this year, when a  before returning home. \u00a9 2024 BBC. The BBC is not responsible for the content of external sites."
    story_generator = initialiseStory(article, storyChain)
    for output in story_generator:
        print(output.content)