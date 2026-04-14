class AnalyzeService:
    def __init__(self, router):
        self.router = router

    def analyze(self, text: str, max_tokens: int = 256) -> str:
        prompt = (
            "You are an analysis assistant. "
            "Provide a clear and direct answer.\n\n"
            f"{text}"
        )
        result = self.router.generate(prompt, max_tokens=max_tokens)
        return result["text"]