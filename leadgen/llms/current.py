from .openai import openAIProvider
from .llama import llamaProvider
import json 

def get_llm_and_embeddings():
    with open('prefs.json', 'r') as f:
        dct = json.load(f)

        if dct['llm'] == openAIProvider.SELECTOR:
            return openAIProvider
        
        elif dct['llm'] == llamaProvider.SELECTOR:
            return llamaProvider

        raise NotImplementedError("The llm you want hasn't been added yet")
    
provider = get_llm_and_embeddings()
            