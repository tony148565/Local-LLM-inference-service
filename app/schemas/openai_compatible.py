# app/schemas/openai_compatible.py

from typing import Literal, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "local-model"
    messages: list[ChatMessage]
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


class ChatCompletionResponseMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: ChatCompletionResponseMessage
    finish_reason: str = "stop"


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]