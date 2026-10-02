from dataclasses import dataclass
from math import hypot
import time

@dataclass
class Track:
    track_id: int
    x: int
    y: int
    w: int
    h: int
    confidence: float
    missed: int = 0
    first_seen: float = 0.0
    last_seen: float = 0.0
    vx: float = 0.0
    vy: float = 0.0

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

class CentroidTracker:
    def __init__(self, max_distance=120, max_missed=12):
        self.max_distance = max_distance
        self.max_missed = max_missed
        self.next_id = 1
        self.tracks: dict[int, Track] = {}
        self.total_detected = 0

    def update(self, detections):
        now = time.time()
        unmatched = set(range(len(detections)))
        pairs = []
        for tid, t in self.tracks.items():
            best_idx = None
            best_dist = self.max_distance
            for idx in unmatched:
                d = detections[idx]
                dcx = d["x"] + d["w"] / 2
                dcy = d["y"] + d["h"] / 2
                dist = hypot(t.cx - dcx, t.cy - dcy)
                if dist < best_dist:
                    best_dist = dist
                    best_idx = idx
            if best_idx is not None:
                pairs.append((tid, best_idx))
                unmatched.remove(best_idx)

        for tid, idx in pairs:
            d = detections[idx]
            t = self.tracks[tid]
            old_cx, old_cy = t.cx, t.cy
            new_cx = d["x"] + d["w"] / 2
            new_cy = d["y"] + d["h"] / 2
            t.vx, t.vy = new_cx - old_cx, new_cy - old_cy
            t.x, t.y, t.w, t.h = d["x"], d["y"], d["w"], d["h"]
            t.confidence = d["confidence"]
            t.missed = 0
            t.last_seen = now
            self.total_detected += 1

        for tid, t in list(self.tracks.items()):
            if not any(p[0] == tid for p in pairs):
                t.missed += 1
                t.last_seen = now
                if t.missed > self.max_missed:
                    del self.tracks[tid]

        for idx in unmatched:
            d = detections[idx]
            tid = self.next_id
            self.next_id += 1
            self.tracks[tid] = Track(
                track_id=tid, x=d["x"], y=d["y"], w=d["w"], h=d["h"],
                confidence=d["confidence"], first_seen=now, last_seen=now
            )
            self.total_detected += 1

        return list(self.tracks.values())
