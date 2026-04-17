from pydantic import BaseModel
from typing import Optional


class Track2EventRequest(BaseModel):
    video_path: Optional[str] = None
    model_path: Optional[str] = None
    tracks_path: Optional[str] = None
    analyze_path: Optional[str] = None
    events_path: Optional[str] = None