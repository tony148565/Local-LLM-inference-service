from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)


class AnalyzeResponse(BaseModel):
    content: str
    backend: str