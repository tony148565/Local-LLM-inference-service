# app/api/openai_compatible.py

import time
import uuid

from fastapi import APIRouter, HTTPException

from app.config import MAX_TOKENS
from app.dependencies import router
from app.schemas.openai_compatible import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatCompletionResponseMessage,
)


router_api = APIRouter(prefix="/v1")


def messages_to_prompt(messages) -> str:
    parts = []

    for msg in messages:
        if msg.role == "system":
            parts.append(f"System: {msg.content}")
        elif msg.role == "user":
            parts.append(f"User: {msg.content}")
        elif msg.role == "assistant":
            parts.append(f"Assistant: {msg.content}")

    parts.append("Assistant:")
    return "\n".join(parts)


@router_api.post("/chat/completions", response_model=ChatCompletionResponse)
def chat_completions(req: ChatCompletionRequest):
    if req.stream:
        raise HTTPException(
            status_code=400,
            detail="stream=true is not supported yet",
        )

    try:
        prompt = messages_to_prompt(req.messages)

        result = router.generate(
            prompt,
            max_tokens=req.max_tokens or MAX_TOKENS,
        )

        content = result["text"]

        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            created=int(time.time()),
            model=req.model,
            choices=[
                ChatCompletionChoice(
                    message=ChatCompletionResponseMessage(
                        content=content,
                    )
                )
            ],
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc