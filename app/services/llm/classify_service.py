import json
from app.schemas import TextAnalysisResult

class ClassifyService:
    def __init__(self, router):
        self.router = router

    def classify(self, text: str, max_tokens: int = 256) -> TextAnalysisResult:
        prompt = f"""
Return ONLY valid JSON. No explanation.

Schema:
{{
  "topic": "string",
  "sentiment": "positive | neutral | negative",
  "urgency": "low | medium | high"
}}

Text:
{text}
"""

        last_error = None

        for _ in range(2):
            result = self.router.generate(prompt, max_tokens=max_tokens)
            text_output = result["text"].strip()
            print("RAW LLM OUTPUT:", text_output)

            if not text_output:
                last_error = ValueError("LLM returned empty response")
                continue

            try:
                data = json.loads(text_output)
                return TextAnalysisResult(**data)
            except (json.JSONDecodeError, ValueError, TypeError) as exc:
                last_error = exc
                continue

        raise RuntimeError(f"Failed to get valid structured output: {last_error}")