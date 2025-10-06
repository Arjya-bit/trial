from pathlib import Path
from typing import Any, Dict

from src.core.config import get_settings
from src.modules.ai_model.model_downloader import bootstrap_model_assets
from src.utils.logger import get_logger

LOGGER = get_logger(__name__)


class ModelService:
    def __init__(self) -> None:
        self.ready = False
        self.model_path: Path | None = None
        self._init_model()

    def _init_model(self) -> None:
        settings = get_settings()
        if settings.model_file and Path(settings.model_file).exists():
            self.model_path = Path(settings.model_file)
            self.ready = True
            LOGGER.info("Using existing model file at %s", self.model_path)
            return
        assets_dir = bootstrap_model_assets()
        if assets_dir:
            # Placeholder: pick first file as model
            for p in assets_dir.iterdir():
                if p.is_file():
                    self.model_path = p
                    self.ready = True
                    LOGGER.info("Model initialized from %s", p)
                    break

    def status(self) -> Dict[str, Any]:
        return {
            "ready": self.ready,
            "model_path": str(self.model_path) if self.model_path else None,
        }

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.ready:
            return {"error": "model not ready"}
        # Placeholder prediction logic
        return {"echo": payload, "model": str(self.model_path)}
