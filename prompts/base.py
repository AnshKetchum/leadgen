from typing import List
from langchain import PromptTemplate
from llm import llm
import re 
from langchain.prompts import StringPromptTemplate
from langchain.llms.base import LLM


template = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Answer the following questions as best you can. You have access to the following tools:

1. LinkedIn requesting

Strictly use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [FinDBQA]
Action Input: the input to the action, it should follow the instructions from the tools.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

For examples:
Question: How old is CEO of Microsoft wife?
Thought: First, I need to find who is the CEO of Microsoft.
Action: Google Search
Action Input: Who is the CEO of Microsoft?
Observation: Satya Nadella is the CEO of Microsoft.
Thought: Now, I should find out Satya Nadella's wife.
Action: Google Search
Action Input: Who is Satya Nadella's wife?
Observation: Satya Nadella's wife's name is Anupama Nadella.
Thought: Then, I need to check Anupama Nadella's age.
Action: Google Search
Action Input: How old is Anupama Nadella?
Observation: Anupama Nadella's age is 50.
Thought: I now know the final answer.
Final Answer: Anupama Nadella is 50 years old.

### Input:
{input}

### Response:
{agent_scratchpad}"""

temp_Ins = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Question: {thought}
Query: {query}
Observation: {observation}

### Input:
Make a short summary of useful information from the result observation that is related to the question.

### Response:"""

prompt_Ins = PromptTemplate(
    input_variables=["thought", "query", "observation"],
    template=temp_Ins,
)

class CustomPromptTemplate(StringPromptTemplate):

    input_variables: List[str]
    """A list of the names of the variables the prompt template expects."""

    template: str
    """The prompt template."""

    template_format: str = "f-string"
    """The format of the prompt template. Options are: 'f-string', 'jinja2'."""

    validate_template: bool = False
    """Whether or not to try validating the template."""

    llm: LLM

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        # Refine the observation

        if len(intermediate_steps) > 0:
            regex = r"Thought\s*\d*\s*:(.*?)\n*Action\s*\d*\s*:(.*?)\n*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            text_match = intermediate_steps[-1][0].log
            if len(intermediate_steps) > 1:
                text_match = 'Thought: ' + text_match

            
            match = re.search(regex, text_match, re.DOTALL)  

            if not match:
                regex2 = r"Thought\s*\d*\s*:(.*?)\n*Action\s*\d*\s*:(.*?)\n*Input\s*\d*\s*:[\s]*(.*)"
                match = re.search(regex2, text_match, re.DOTALL)


            my_list = list(intermediate_steps[-1])

            print('match', match)

            p_INS_temp = prompt_Ins.format(thought=match.group(1).strip(), query=match.group(3).strip(), observation=my_list[1])

            print('fed', p_INS_temp)

            my_list[1] = self.llm(p_INS_temp)
            my_tuple = tuple(my_list)            
            intermediate_steps[-1] = my_tuple
            
        for action, observation in intermediate_steps:
            thoughts += action.log

            print('observation: ', observation, action.log)
            thoughts += f" {observation}\nThought:"
        
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts

        formatted = self.template.format(**kwargs)
        print(formatted)

        return formatted
    
    
prompt = CustomPromptTemplate(input_variables=["input", "intermediate_steps"], template=template,validate_template=False, llm=llm)