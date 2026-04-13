import time
from llama_cpp import Llama


class LocalLLMService:
    def __init__(self, model_path: str, n_ctx: int, n_gpu_layers: int, verbose: bool = False):
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose

        if not self.model_path:
            raise ValueError("MODEL_PATH is not set")

        self.warmup_ok = False
        self.warmup_error = None

        load_start = time.time()
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            verbose=self.verbose,
        )
        self.loaded_time = time.time() - load_start

        try:
            _ = self.llm.create_chat_completion(
                messages=[
                    {"role": "user", "content": "Reply with exactly one word: ready"}
                ],
                max_tokens=8,
            )
            self.warmup_ok = True
        except Exception as exc:
            self.warmup_error = str(exc)

    def analyze(self, text: str, max_tokens: int = 256) -> str:
        try:
            result = self.llm.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an analysis assistant. "
                            "Provide a clear and direct answer."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                max_tokens=max_tokens,
            )
            return result["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            raise RuntimeError(f"Local LLM inference failed: {exc}") from exc

    def health(self) -> dict:
        return {
            "backend": "llama_cpp_local",
            "model_path": self.model_path,
            "n_ctx": self.n_ctx,
            "n_gpu_layers": self.n_gpu_layers,
            "loaded_time_sec": round(self.loaded_time, 3),
            "warmup_ok": self.warmup_ok,
            "warmup_error": self.warmup_error,
        }