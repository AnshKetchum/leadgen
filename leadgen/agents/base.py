from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory

from ..tools.linkedin.tool import ObtainLinkedInDataTool, create_qa_retriever_tool
from ..templates.base import TEMPLATE

#Env
import os
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo", max_tokens=2048, openai_api_key=os.getenv("OPENAI_API_KEY"))
tools = [ ObtainLinkedInDataTool(), create_qa_retriever_tool(llm)]

prompt = ChatPromptTemplate.from_messages([
    ("system", TEMPLATE),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("human", "{input}")
])

memory = ConversationBufferWindowMemory(
                                    memory_key='chat_history',
                                    return_messages=True,
                                    k=6
                                  )

def get_chain():
    agent = OpenAIFunctionsAgent(llm=ChatOpenAI(temperature=0, model="gpt-4"), prompt=prompt, tools=tools)
    agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=5, early_stopping_method="generate", memory=memory)
    return agent_executor

agent = get_chain()