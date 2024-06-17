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

def initialiseModel(llm, output_parser):
    load_dotenv()
    
    # llm = AzureChatOpenAI(
    #     api_version = os.getenv("OPENAI_API_VERSION"), 
    #     api_key = os.getenv("AZURE_API_KEY"),
    #     azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    #     azure_deployment="StoryGPT3"
    # )

    # #llm = ChatOpenAI(openai_api_key = os.getenv("OPENAI_API_KEY"), model = "gpt-3.5-turbo-0125")
    # output_parser = StrOutputParser() #converts output to string
    memory = ConversationBufferWindowMemory(k=4, ai_prefix="Narrator")#ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = """
    The following is an interactive educational children's story-telling session between a 6-10 year old child reader and the narrator. The reader will give you a news article and your goal is to be the narrator 
    and to create and continue a short interactive story based on the main topic of a news article. Respond with only a part of the story (1 page approx 100-300 words) with room for continuation. 
    Start the page with a visual description of the page for prompting an image model beginning with "DALL-E Prompt: ". Then start the story with "STORY: ". Don't forget to introduce the context of the story by talking about
    the news article briefly, assume the reader hasn't read the article. At the end of the page, either end the story with "THE END" or continue by
    asking an educational question to the reader such as making a decision that will change the next page of the story. Start this with "Question: ". No matter what response the reader gives, be the narrator for a children's story
    with the age range fixed at 7-12 year olds. Also always output the educational topics and genres that summarise the response starting with  "Themes: "

    Current conversation: {history}
    Reader: {input}
    Narrator: 
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
        
def initialiseStory(article, storyChain):
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

    response = storyChain(article)
    return response["response"]

def continueStory(storyChain, userInput):
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
    response = storyChain(userInput)
    print(response["response"])
    return response["response"]



#Testing:

if __name__ == "__main__":
    storyChain = initialiseModel()
    article = '''The Asian hornet looks quite different from our native hornets The insects are an invasive species, which means they are from outside the UK and are a threat to native wildlife, such as bees and wasps.  
                Last summer there were record amounts of Asian hornet sightings in the UK. The UK's chief plant health officer, Nicola Spence, has asked people to report any sightings of the hornet to a special helpline. 
                Here's an Asian hornet for scale next to a bee - the hornet is on the left Asian hornets are slightly smaller than the native hornets we have in the UK. The Wildlife Trust says they have an orange head, a 
                dark abdomen, and legs with yellow tips. The government's environment department, Defra, recommends that if you think you see one, report it to their helpline. If you're out and about and you think you've 
                spotted an Asian hornet, ask an adult you trust to take a picture of it, and to find the helpline. Don't try to get nearer to take a photo yourself. Defra says that Asian hornets are no less dangerous to 
                humans than native hornets that we see in the UK every summer. However, they can be very dangerous to our local wildlife. Asian hornets can pose a big threat to bee colonies An invasive species is something 
                that comes from a different ecosystem, like another country, and takes over native animals habitats and food. This can be dangerous to native wildlife.  Native is the term used when something lives in the place 
                it comes from. For example, oak trees are native to the UK. Invasive species can have a damaging impact on biodiversity. This is because when they kill other species or take their food and habitat, they take 
                over the population, making it harder for smaller species to develop or thrive. Grey squirrels are an invasive species from the USA Imagine the natural world as a computer, made up of lots of different parts 
                that all work to help each other.  Worms create and improve the soil for plants to grow in, but they are also food for birds, and birds provide food for larger predators. Trees that grow in the soil also make 
                homes for birds - and provide tasty food too.  This happens on a big scale all over the world. If you take away one part of the ecosystem, there could be big consequences for lots of different creatures.  
                One species being wiped out by an invasive one could lead to another species losing its food, or animals losing their homes.  Like a computer, if you take one part out of an ecosystem, it may struggle do the 
                job that it's meant to.  The Chinese mitten crab - named for its furry-looking claws - is an invasive species here in the UK An organisation called the Wildlife and Countryside Link has warned that climate change
                  - bringing warmer temperatures and increased flooding - has lead to other invasive species growing in the UK.  You might have heard of Japanese Knotweed - it's a super invasive plant that can quickly take over 
                  gardens and green spaces. It's got a tough network of roots underground which can make it very difficult to get rid of once it's there, and it can cause damage to buildings.  Another is Himalayan Balsam, 
                  which causes problems for native plants in the UK. It grows really quickly and takes over the habitats of other plants. Because it grows near riverbanks, it can also increase the risk of flooding. There's 
                  also Giant Hogweed - which people have been told to look out for because it can cause burns on the skin. The Woodland Trust recommends that people learn what it looks like, and try to avoid brushing past 
                  it when you're out exploring nature.  This is a giant hogweed - they can grow pretty tall - up to five metres The Woodland Trust recommends you get medical help as soon as you can if you think you have been 
                  burned by Giant Hogweed. You can always ask an adult you trust if you're unsure. Invasive species are already one of the biggest threats to the UK environment Richard Benwell, Wildlife and Countryside Link 
                  Charities and environmental groups have asked the government to help protect native species from invasive ones.  The River Trust, Plantlife and Buglife are all calling for Invasive Species Week (20-26 May) 
                  to be recognised to help raise awareness of the threats against UK wildlife. The government has a list of invasive non-native species that threaten wildlife in the UK. There's strict rules around them, and 
                  you're not allowed to do things like keep them as pets or sell them. Comments can not be loaded To load Comments you need to enable JavaScript in your browser \u00a9 2024 BBC. The BBC is not responsible for 
                  the content of external sites." '''

    # Initializing story with the article
    print("Starting story...")
    for part in initialiseStory(article, storyChain):
        print(part, end='')

    # Continuing story with user input
    while True:
        user_input = input("\nUser input: ")
        if user_input.lower() == "exit":
            break
        for part in continueStory(storyChain, user_input):
            print(part, end='')
        if "THE END" in part:
            break
    
# def saveToMemory(memory, new_content):
#     # Retrieve existing story history from memory
#     existingHistory = memory.load_memory_variables({"input": "history"})
#     updatedHistory = existingHistory.get("history", "") + " " + new_content
    
#     # Now save the updated history back into memory
#     memory.save_context({"input": "history"}, {"output": updatedHistory})
#     print("Updated story history saved to memory.")
