from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def get_llm():
        '''
        Factory method to create an LLM 
        '''
        pass 

    @abstractmethod
    def get_embeddings():
        '''
        Factory method to create an LLM 
        '''
        pass 