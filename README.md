# Face Tracking System — Full Stack Reference Implementation

A runnable research/prototyping implementation inspired by the supplied dashboard UI. It provides a dark monitoring dashboard, browser camera capture, real-time face detection/tracking through FastAPI WebSockets, analytics, tracked-face cards, settings, and a lightweight REST API.

> **Privacy note:** This implementation performs face *detection and temporary tracking IDs*. It does not perform biometric identification or infer identity attributes. Do not deploy it for consequential decisions without appropriate legal, privacy, security, and accuracy review.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + OpenCV + NumPy
- Realtime: WebSocket (`/ws/track`)
- Tracking: centroid-based multi-object tracker with stable session IDs
- Detection: OpenCV Haar cascade (`haarcascade_frontalface_default.xml`)
- Containerization: Docker Compose

## Project structure

```text
face-tracking-system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── detector.py
│   │   ├── tracker.py
│   │   ├── schemas.py
│   │   └── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/ui-reference.png
├── docker-compose.yml
└── .env.example
```

## Run locally

### Backend

Python 3.11+ is recommended.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

Node 20+ is recommended.

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The browser will request camera permission. If camera access is unavailable, the dashboard remains usable in demo mode with simulated metrics and no real tracking frames.

## Docker

```bash
docker compose up --build
```

Open `http://localhost:5173`.

## API

- `GET /api/health` — health check
- `GET /api/summary` — current tracking summary
- `GET /api/tracks` — active/recent tracks
- `GET /api/analytics` — time-series analytics
- `WS /ws/track` — accepts JPEG/base64 frames and returns detections/tracks

WebSocket message sent by the frontend:

```json
{"type":"frame","image":"data:image/jpeg;base64,..."}
```

Response:

```json
{
  "type": "result",
  "width": 1280,
  "height": 720,
  "faces": [
    {"track_id": 1, "x": 120, "y": 90, "w": 160, "h": 190, "confidence": 0.93, "status": "tracking"}
  ],
  "fps": 24.1
}
```

## Production/research extensions

This reference implementation intentionally uses a lightweight OpenCV detector so it can run without proprietary weights. For a research-grade system, replace `detector.py` with a validated detector/landmark model and benchmark it on a documented dataset. Add proper authentication, TLS, access control, audit logging, encrypted storage, model versioning, monitoring, rate limiting, and privacy controls before deployment.
