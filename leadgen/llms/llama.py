from .base import BaseLLM

N_BATCH = 2**7 
N_GPU_LAYERS = 10 
NUM_CONTEXT = 2**12
TEMPERATURE = 0
MODEL_PATH = "./models/llama-2-13b-chat.Q5_K_M.gguf"
STOP_WORDS = ["\nHuman:", "\nAI:", "\nAssistant:", "\nYou:"]


class LLaMALLM(BaseLLM):
    SELECTOR = "llama"

    def __init__(self) -> None:
        super().__init__()

        from langchain.llms.llamacpp import LlamaCpp 
        from langchain.embeddings.llamacpp import LlamaCppEmbeddings
        
        self.llm = LlamaCpp(
                    model_path=MODEL_PATH,
                    n_gpu_layers=N_GPU_LAYERS,
                    n_batch=N_BATCH,
                    n_ctx=NUM_CONTEXT,
                    temperature=TEMPERATURE,
                    stop=STOP_WORDS,
                    f16_kv=True,
                    verbose=True,
                    n_parts=-1,
                    streaming=True,
                )

        self.embeddings = LlamaCppEmbeddings(
                model_path=MODEL_PATH,
                n_gpu_layers=N_GPU_LAYERS,
                n_batch=N_BATCH,
                n_ctx=NUM_CONTEXT,
                f16_kv=True,
                verbose=True,
                n_parts=-1
            )

    def get_llm(self):
        return self.llm

    def get_embeddings(self):
        return self.embeddings

