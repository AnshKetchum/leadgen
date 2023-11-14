from langchain.llms import OpenAI
from config import OPENAI_API_KEY

llm = OpenAI(temperature=0.7, openai_api_key= OPENAI_API_KEY)