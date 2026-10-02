import base64
import time
from collections import deque

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .detector import FaceDetector
from .schemas import FaceTrack
from .tracker import CentroidTracker

app = FastAPI(title=settings.app_name, version=settings.version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

detector = FaceDetector(
    settings.detector_scale_factor,
    settings.detector_min_neighbors,
    settings.detector_min_size,
)
tracker = CentroidTracker()
metrics = {"frames": 0, "fps": 0.0, "last_ts": time.time(), "conf": deque(maxlen=60), "series": deque(maxlen=60)}

@app.get("/api/health")
def health():
    return {"status": "online", "service": settings.app_name, "version": settings.version}

@app.get("/api/summary")
def summary():
    active = [t for t in tracker.tracks.values() if t.missed == 0]
    avg = sum(t.confidence for t in active) / len(active) if active else 0.0
    return {
        "active_faces": len(active),
        "faces_detected": tracker.total_detected,
        "tracking_fps": round(metrics["fps"], 1),
        "average_confidence": round(avg * 100, 1),
        "camera": "Browser Camera",
        "processing": "CPU",
    }

@app.get("/api/tracks")
def tracks():
    return [FaceTrack(track_id=t.track_id, x=t.x, y=t.y, w=t.w, h=t.h, confidence=t.confidence, status="lost" if t.missed else "tracking").model_dump() for t in tracker.tracks.values()]

@app.get("/api/analytics")
def analytics():
    points = list(metrics["series"])
    return {"points": points}

def decode_data_url(data: str):
    if "," in data:
        data = data.split(",", 1)[1]
    raw = base64.b64decode(data)
    if len(raw) > settings.max_frame_bytes:
        raise ValueError("Frame too large")
    arr = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Invalid JPEG frame")
    return frame

@app.websocket("/ws/track")
async def track_socket(ws: WebSocket):
    await ws.accept()
    previous = time.perf_counter()
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("type") != "frame":
                continue
            frame = decode_data_url(msg.get("image", ""))
            detections = detector.detect(frame)
            tracks = tracker.update(detections)
            now = time.perf_counter()
            dt = max(1e-3, now - previous)
            previous = now
            instant_fps = 1.0 / dt
            metrics["fps"] = metrics["fps"] * 0.85 + instant_fps * 0.15
            metrics["frames"] += 1
            active = [t for t in tracks if t.missed == 0]
            avg_conf = sum(t.confidence for t in active) / len(active) if active else 0
            metrics["conf"].append(avg_conf)
            metrics["series"].append({"t": time.time(), "detected": len(detections), "tracked": len(active), "confidence": round(avg_conf * 100, 1)})
            payload = {
                "type": "result",
                "width": int(frame.shape[1]),
                "height": int(frame.shape[0]),
                "faces": [
                    {"track_id": t.track_id, "x": t.x, "y": t.y, "w": t.w, "h": t.h, "confidence": round(t.confidence, 3), "status": "lost" if t.missed else "tracking"}
                    for t in tracks
                ],
                "fps": round(metrics["fps"], 1),
            }
            await ws.send_json(payload)
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await ws.close(code=1011, reason=str(exc)[:120])
