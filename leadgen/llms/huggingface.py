from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .base import BaseLLM

STOP_WORDS = ["\nHuman"]

def get_provider(model_id):
    model_id = model_id #"gpt2"
    hf = HuggingFacePipeline.from_model_id(
            model_id=model_id,
            task="text-generation",
            device=0,
            batch_size=2, 
        )

    template = """Question: {question}

    Answer: Let's think step by step."""
    chain = PromptTemplate.from_template(template) | hf

    embeddings = HuggingFaceEmbeddings()


    class HFLLM(BaseLLM):
        SELECTOR = "huggingface"

        def get_llm():
            return chain

        def get_embeddings():
            return embeddings
    
    return HFLLM