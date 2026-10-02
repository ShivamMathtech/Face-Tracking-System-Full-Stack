import cv2
import numpy as np

class FaceDetector:
    """Lightweight face detector for the reference implementation.

    It detects faces but does not identify people. Confidence is derived from
    detection size/quality as a UI-friendly proxy, not a calibrated probability.
    """
    def __init__(self, scale_factor=1.1, min_neighbors=5, min_size=(45, 45)):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        if self.cascade.empty():
            raise RuntimeError(f"Unable to load Haar cascade from {cascade_path}")
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, frame: np.ndarray):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        boxes = self.cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
        )
        h, w = frame.shape[:2]
        results = []
        frame_area = max(1, w * h)
        for x, y, bw, bh in boxes:
            area_ratio = (bw * bh) / frame_area
            # UI-only confidence heuristic. Not a calibrated model score.
            confidence = min(0.99, max(0.55, 0.70 + area_ratio * 4.0))
            results.append({"x": int(x), "y": int(y), "w": int(bw), "h": int(bh), "confidence": confidence})
        return results
