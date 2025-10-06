from __future__ import annotations
from pathlib import Path
from typing import Any
import joblib

from .model_downloader import download_model

_model = None


def _load_model() -> Any | None:
    global _model
    if _model is not None:
        return _model
    model_path = download_model()
    if model_path and Path(model_path).exists():
        try:
            _model = joblib.load(model_path)
            return _model
        except Exception:
            return None
    return None


def predict_text(text: str) -> dict:
    model = _load_model()
    if model is None:
        # Fallback dummy behavior
        return {"label": "neutral", "confidence": 0.5}

    try:
        pred = model.predict([text])[0]
        if hasattr(model, "predict_proba"):
            proba = float(max(model.predict_proba([text])[0]))
        else:
            proba = 0.9
        return {"label": str(pred), "confidence": proba}
    except Exception:
        return {"label": "error", "confidence": 0.0}
