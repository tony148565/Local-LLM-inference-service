from fastapi import APIRouter, HTTPException

from app.schemas.track2event import Track2EventRequest
from app.dependencies import track2event_service

router_api = APIRouter()


@router_api.post("/track2event")
def track2event(req: Track2EventRequest):
    try:
        return track2event_service.run(req.model_dump(exclude_none=True))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc