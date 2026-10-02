from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Face Tracking System API"
    version: str = "1.0.0"
    max_frame_bytes: int = 4_000_000
    jpeg_quality: int = 80
    detector_scale_factor: float = 1.1
    detector_min_neighbors: int = 5
    detector_min_size: tuple[int, int] = (45, 45)

settings = Settings()
