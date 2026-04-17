# legacy reference only
# do not import from this file


from pydantic import BaseModel, Field
from typing import Optional

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)


class AnalyzeResponse(BaseModel):
    content: str
    backend: str

class TextAnalysisResult(BaseModel):
    topic: str
    sentiment: str
    urgency: str

class Track2EventRequest(BaseModel):
    video_path: Optional[str] = None
    model_path: Optional[str] = None
    tracks_path: Optional[str] = None
    analyze_path: Optional[str] = None
    events_path: Optional[str] = None

    fps: float = Field(23.98, gt=0)
    min_track_points: int = Field(5, ge=1)
    max_frame_gap: int = Field(5, ge=0)
    max_speed: float = Field(300.0, gt=0)
    min_duration: float = Field(3.0, ge=0)
    stationary_max_speed: float = Field(10.0, ge=0)
    stationary_max_distance: float = Field(50.0, ge=0)
    verbose: bool = True