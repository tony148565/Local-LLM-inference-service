from llama_cpp import Llama
import time
from ..base import LLMBackend

class LocalBackend(LLMBackend):
    def __init__(self, model_path: str, n_ctx: int, n_gpu_layers: int, verbose: bool = False):
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose

        if not self.model_path:
            raise ValueError("MODEL_PATH is not set")
        
        load_start = time.time()
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            verbose=self.verbose,
        )
        self.loaded_time = time.time() - load_start

    def generate(self, prompt: str, max_tokens: int = 256) -> dict:
        try:
            result = self.llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return {
                "text": result["choices"][0]["message"]["content"].strip(),
                "raw": result,
            }
        except Exception as exc:
            raise RuntimeError(f"Local LLM inference failed: {exc}") from exc

    def health(self) -> dict:
        return {
            "backend": "local",
            "model_path": self.model_path,
            "n_ctx": self.n_ctx,
            "n_gpu_layers": self.n_gpu_layers,
            "loaded_time_sec": round(self.loaded_time, 3)
        }