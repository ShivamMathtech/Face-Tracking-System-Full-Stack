# Development notes

The supplied UI is reproduced as a responsive React dashboard rather than a pixel-perfect screenshot renderer. The live video area uses the user's browser camera and overlays backend-returned detections in the API layer; the first version intentionally keeps the actual overlay minimal so the browser stream remains smooth.

For a research version, recommended next steps are: replace Haar detection with a validated detector/landmark model; add camera calibration and tracking evaluation; persist telemetry; add automated tests; and conduct a privacy/security review.
