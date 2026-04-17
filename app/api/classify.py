from fastapi import APIRouter, HTTPException

from app.config import MAX_TOKENS
from app.schemas.analyze import AnalyzeRequest
from app.schemas.classify import TextAnalysisResult
from app.dependencies import classify_service

router_api = APIRouter()


@router_api.post("/classify", response_model=TextAnalysisResult)
def classify(req: AnalyzeRequest):
    try:
        return classify_service.classify(req.text, max_tokens=MAX_TOKENS)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc