
from langchain import LLMChain
from langchain.agents import LLMSingleActionAgent, AgentExecutor 
from tool import tool_names
from prompt import prompt
from llm import llm 
from output import output_parser 

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tool_names, verbose=True)

agent_executor.run("Tell me about the documents in the database.")