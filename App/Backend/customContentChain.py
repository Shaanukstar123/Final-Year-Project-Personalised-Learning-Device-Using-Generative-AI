from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

def initCustomContentModel(llm, output_parser):
    memory = ConversationBufferWindowMemory(k=4)#ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = '''
    You must create educational content based on the "Query" that the user provides you. The content be in any form of text such as stories, riddles, problems, explanations. Give the user freedom to choose if it's appropriate and keep them engaged. User is 7-12 years old so make it appropriate and fun.
    Try to add an image to the page when necessary by writing a single "Image Prompt: " at the start of your response with a description of the image necessary. Talk directly to the user at all times. This is a continuos conversation so only ask one question at a time and wait for a response.
    Current conversation: {history}
    Child: {input}
    '''
    prompt = PromptTemplate(input_variables=["history", "input"], template=promptText)
    #story chain with llm, prompt and memory with output parser as string
    customChain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        output_parser=output_parser,
        verbose=True
    )
    #storyChain = ConversationChain(llm=llm, prompt=prompt, memory=memory)
    print("CustomCont Model initialised")
    return customChain

def initialiseCustomContent(customChain, topic):
    #clear the memory
    customChain.memory.clear()
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

    response = customChain(topic)
    return response["response"]

def continueCustomContent(customChain, userInput):
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
    response = customChain(userInput)
    print(response["response"])
    return response["response"]