from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

def initCustomContentModel(llm, output_parser):
    memory = ConversationBufferWindowMemory(k=4)#ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = '''
    You must create educational content based on the "Query" that the user provides you. The content be in any form of text such as stories, riddles, problems, explanations. Give the user freedom to choose if it's appropriate and keep them engaged. User is 7-12 years old so make it appropriate and fun.
    Occasionally add an image to the page when necessary by writing a single "Image Prompt: " at the start of your response with a description of the image necessary. Talk directly to the user at all times.
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