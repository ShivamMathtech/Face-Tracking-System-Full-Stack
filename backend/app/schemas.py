from pydantic import BaseModel, Field
from typing import Literal

class FaceTrack(BaseModel):
    track_id: int
    x: int
    y: int
    w: int
    h: int
    confidence: float = Field(ge=0, le=1)
    status: Literal["tracking", "lost", "new"] = "tracking"

class TrackSummary(BaseModel):
    active_faces: int
    faces_detected: int
    tracking_fps: float
    average_confidence: float
    camera: str
    processing: str
