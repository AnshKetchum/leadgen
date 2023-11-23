from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents import ZeroShotAgent
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str, format_log_to_messages
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import StreamlitChatMessageHistory
from langchain.schema.messages import FunctionMessage

from langchain.callbacks import StreamlitCallbackHandler, FinalStreamingStdOutCallbackHandler

from ..tools.linkedin.tool import ObtainLinkedInDataTool, LinkedInJobRetrievalTool 
from ..templates.base import TEMPLATE
from ..tools.general.tool import local_vectorstore_retrieval
from ..tools.general.misc import general_tools
from ..tools.outreach.mail.gmail import tools as gmail_tools
from ..tools.resume.jsonres import CreateResumeTool
from ..tools.cover_letter.gen import CreateCoverLetterTool


import streamlit as st

#Env
import os
from dotenv import load_dotenv

from leadgen.llms.current import provider
from leadgen.db.JobsDatabase import JobsDatabase
from leadgen.db.UsersDatabase import UsersDatabase

from langchain.chat_models import ChatOpenAI

load_dotenv()


def get_chain(retriever = None, streamlit_container = None, email = True):

    db = JobsDatabase(provider)
    db_user = UsersDatabase(provider)
    llm = provider.get_llm()
    
    tools = [ 
            CreateResumeTool(),
            CreateCoverLetterTool(userdb = db_user), 
            *general_tools,
            *db.get_toolkit(),
        ]
    
    if retriever:
        tools.append(local_vectorstore_retrieval(retriever))

    if email:
        tools.extend(gmail_tools)
    
    print(TEMPLATE)
    prompt = ChatPromptTemplate.from_messages([
        ("system", TEMPLATE),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferWindowMemory(
                                        memory_key='chat_history',
                                        chat_memory= msgs,
                                        return_messages=True,
                                    )

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
        memory=memory,
        callbacks=callbacks,
        handle_parsing_errors=True,
        early_stopping_method="generate",
    )

    return agent_executor

agent = get_chain()