from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

def initCustomContentModel(llm, output_parser):
    memory = ConversationBufferWindowMemory(k=4, ai_prefix="Content Creator")#ConversationSummaryBufferMemory(llm=llm, max_token_limit= 500)
    promptText = '''
    You are a content creator and reader for children's educational content. The user will give you a "Query" and you must to your best ability use that query to generate educational content. This be in any form of text such as stories, riddles, problems, explanations. Give the user freedom to choose if it's appropriate and keep them engaged. User target age: 7-12 years old.
    If any images are needed for narration, write "DALL-E prompt: " and describe the image you want. Talk directly to the user at all times and don't break character.
    Current conversation: {history}
    Child: {input}
    Content Creator: 
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