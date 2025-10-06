import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from src.core.config import get_settings
from src.utils.logger import get_logger

LOGGER = get_logger(__name__)


def ensure_kaggle_credentials() -> bool:
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json.exists():
        return True
    LOGGER.warning("kaggle.json not found. Set OTAFP_KAGGLE_* env or place credentials.")
    return False


def download_kaggle_dataset(dataset: str, dest_dir: str) -> Optional[Path]:
    if not ensure_kaggle_credentials():
        return None

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    cmd = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        dataset,
        "-p",
        str(dest),
        "--unzip",
    ]
    try:
        LOGGER.info("Downloading Kaggle dataset %s to %s", dataset, dest)
        subprocess.check_call(cmd)
        return dest
    except subprocess.CalledProcessError:
        LOGGER.exception("Failed to download Kaggle dataset")
        return None


def bootstrap_model_assets() -> Optional[Path]:
    settings = get_settings()
    if not settings.kaggle_dataset:
        LOGGER.info("No Kaggle dataset configured; skipping download")
        return None
    return download_kaggle_dataset(settings.kaggle_dataset, settings.kaggle_download_dir)
