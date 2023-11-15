from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import StreamlitChatMessageHistory
from langchain.callbacks import StreamlitCallbackHandler, FinalStreamingStdOutCallbackHandler

from ..tools.linkedin.tool import ObtainLinkedInDataTool, LinkedInJobRetrievalTool 
from ..templates.base import TEMPLATE
from ..tools.general.tool import local_vectorstore_retrieval
from ..tools.general.misc import general_tools
from ..tools.outreach.mail.gmail import tools as gmail_tools

#Env
import os
from dotenv import load_dotenv

load_dotenv()


def get_chain(retriever = None, streamlit_container = None, email = True):

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=2048, openai_api_key=os.getenv("OPENAI_API_KEY"))
    tools = [ 
                ObtainLinkedInDataTool(), 
                LinkedInJobRetrievalTool(),
                *general_tools
        ]
    
    if retriever:
        tools.append(local_vectorstore_retrieval(retriever))

    if email:
        tools.extend(gmail_tools)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", TEMPLATE),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])


    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferWindowMemory(
                                        memory_key='chat_history',
                                        chat_memory= msgs,
                                        return_messages=True,
                                    )

    llm=ChatOpenAI(temperature=0, model="gpt-4", streaming=True)

    callbacks = [
        FinalStreamingStdOutCallbackHandler()        
    ]

    if streamlit_container:
        callbacks.append(StreamlitCallbackHandler(streamlit_container))

    agent = OpenAIFunctionsAgent(llm=llm, prompt=prompt, tools=tools)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        max_iterations=5, 
        early_stopping_method="generate", 
        memory=memory,
        callbacks=callbacks
    )

    return agent_executor

agent = get_chain()