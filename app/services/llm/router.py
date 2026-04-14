class LLMRouter:
    def __init__(self, local_backend=None, openai_backend=None, mode: str = "local"):
        self.local_backend = local_backend
        self.openai_backend = openai_backend
        self.mode = mode

    def generate(self, prompt: str, max_tokens: int = 256) -> dict:
        if self.mode == "local":
            if self.local_backend is None:
                raise RuntimeError("Local backend is not configured")
            return self.local_backend.generate(prompt, max_tokens=max_tokens)

        if self.mode == "openai":
            if self.openai_backend is None:
                raise RuntimeError("OpenAI backend is not configured")
            return self.openai_backend.generate(prompt, max_tokens=max_tokens)

        raise ValueError(f"Unknown LLM_BACKEND mode: {self.mode}")