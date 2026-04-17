from fastapi import APIRouter, HTTPException

from app.config import MAX_TOKENS
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.dependencies import analyze_service, router

router_api = APIRouter()


@router_api.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        content = analyze_service.analyze(req.text, max_tokens=MAX_TOKENS)
        return AnalyzeResponse(
            content=content,
            backend=router.mode,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc