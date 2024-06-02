import os
import re
from typing import Any, Iterator, Dict, Callable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda, RunnableSerializable, RunnableConfig
from langchain_core.callbacks.manager import CallbackManagerForChainRun
from langchain_core.messages.ai import AIMessageChunk
from dotenv import load_dotenv
from operator import itemgetter

class RunnableCollector(RunnableLambda):
    def _transform(
        self,
        input: Iterator[AIMessageChunk],
        run_manager: CallbackManagerForChainRun,
        config: RunnableConfig,
        **kwargs: Any,
    ) -> Iterator[AIMessageChunk]:
        final: AIMessageChunk
        got_first_val = False
        for ichunk in input:
            yield ichunk

            if not got_first_val:
                final = ichunk
                got_first_val = True
            else:
                try:
                    final = final + ichunk  # type: ignore[operator]
                except TypeError:
                    final = ichunk

        call_func_with_variable_args(
            self.func, final, config, run_manager, **kwargs
        )


class RunnableFilter(RunnableLambda):
    def __init__(self, filter: Callable[[AIMessageChunk], bool], **kwargs: Any) -> None:
        super().__init__(func=lambda _: None, **kwargs)
        self.filter = filter

    def _transform(
        self,
        input: Iterator[AIMessageChunk],
        run_manager: CallbackManagerForChainRun,
        config: RunnableConfig,
        **kwargs: Any,
    ) -> Iterator[AIMessageChunk]:
        for ichunk in input:
            if self.filter(ichunk):
                yield ichunk


class RunnableMap(RunnableLambda):
    def __init__(self, mapping: Callable[[AIMessageChunk], Any], **kwargs: Any) -> None:
        super().__init__(func=lambda _: None, **kwargs)
        self.mapping = mapping

    def _transform(
        self,
        input: Iterator[AIMessageChunk],
        run_manager: CallbackManagerForChainRun,
        config: RunnableConfig,
        **kwargs: Any,
    ) -> Iterator[Any]:
        for ichunk in input:
            yield self.mapping(ichunk)


def initialiseModel():
    load_dotenv()
    
    llm = AzureChatOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"), 
        api_key=os.getenv("AZURE_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment="StoryGPT3"
    )

    output_parser = StrOutputParser()  # Converts output to string
    memory = ConversationBufferWindowMemory(k=2, ai_prefix="Narrator")
    promptText = """
    The following is an interactive educational children's story-telling session between a 6-10 year old child reader and the narrator. The reader will give you a news article and your goal is to be the narrator 
    and to create and continue a short interactive story based on the main topic of a news article. Respond with only a part of the story (1 page approx 50 words) with room to continue. 
    Start the page with a DALL-E prompt for visualising the current page's events beginning with "DALL-E Prompt: ". Then start the story with "STORY: ". At the end of the page, either end the story with "THE END" or continue by
    asking an educational question to the reader such as making a decision that will change the next page of the story. Start this with "Question: ". No matter what response the reader gives, be the narrator for a children's story
    with the age range fixed at 6-12 year olds.

    Current conversation: {history}
    Reader: {input}
    Narrator: 
    """

    prompt = PromptTemplate(input_variables=["history", "input"], template=promptText)
    storyChain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        output_parser=output_parser,
        verbose=False
    )
    print("Model initialised")
    return storyChain

def streamStoryOutput(llm, prompt):
    for output in llm.stream(prompt):
        yield output.content  # Extract the content as a string

def initialiseStory(article, storyChain):
    buffered_output = ""
    for output in streamStoryOutput(storyChain.llm, article):
        buffered_output += output
        while True:
            match = re.search(r'\s', buffered_output)
            if not match:
                break
            index = match.start()
            yield buffered_output[:index + 1]
            buffered_output = buffered_output[index + 1:]

    if buffered_output:
        yield buffered_output

def continueStory(storyChain, userInput):
    print("Continuing story...")
    buffered_output = ""
    for output in streamStoryOutput(storyChain.llm, userInput):
        buffered_output += output
        while True:
            match = re.search(r'\s', buffered_output)
            if not match:
                break
            index = match.start()
            yield buffered_output[:index + 1]
            buffered_output = buffered_output[index + 1:]

    if buffered_output:
        yield buffered_output

def setup_chain(model="gpt-3.5-turbo"):
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)

    def save_into_mem(input_output: Dict[str, Any]):
        message = input_output.pop("output")
        memory.save_context(input_output, {"output": message.content})
        print("\n\n2.\t", memory.load_memory_variables({}))

    chain = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
            dummy=RunnableLambda(lambda x: print("input?", x)),
        )
        | ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_MESSAGE),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{input}"),
            ]
        )
        | ChatOpenAI(
            model=model,
            temperature=0,
            streaming=True,
        )
    )

    chain = (
        RunnablePassthrough.assign(
            output=chain,
        )
        | RunnableFilter(
            filter=lambda chunk: isinstance(chunk, dict) and ("output" in chunk or "input" in chunk)
        )
        | RunnableCollector(save_into_mem)
        | RunnableFilter(
            filter=lambda chunk: isinstance(chunk, dict) and "output" in chunk and "input" not in chunk
        )
        | RunnableMap(mapping=lambda chunk: chunk["output"])
    )

    return chain

if __name__ == "__main__":
    storyChain = initialiseModel()
    article = '''The Asian hornet looks quite different from our native hornets ...'''

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
