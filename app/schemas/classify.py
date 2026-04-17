from pydantic import BaseModel


class TextAnalysisResult(BaseModel):
    topic: str
    sentiment: str
    urgency: str