from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from .base import BaseLLM
from config import OPENAI_API_KEY


class OpenAILLM(BaseLLM):
    SELECTOR = "openai"

    def __init__(self) -> None:
        super().__init__()
        self.llm = ChatOpenAI(temperature=0.7, openai_api_key = OPENAI_API_KEY)
        self.embeddings = OpenAIEmbeddings()


    def get_llm(self,):
        return self.llm 

    def get_embeddings(self,    ):
        return self.embeddings

openAIProvider = OpenAILLM()