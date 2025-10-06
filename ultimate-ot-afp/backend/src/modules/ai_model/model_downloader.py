import os
import subprocess
from pathlib import Path
from ...core.config import settings

KAGGLE_DIR = Path.home() / ".kaggle"
KAGGLE_JSON = KAGGLE_DIR / "kaggle.json"
MODELS_DIR = Path(__file__).resolve().parent


def ensure_kaggle_credentials() -> None:
    if settings.kaggle_username and settings.kaggle_key:
        KAGGLE_DIR.mkdir(parents=True, exist_ok=True)
        KAGGLE_JSON.write_text(
            f"{{\n  \"username\": \"{settings.kaggle_username}\",\n  \"key\": \"{settings.kaggle_key}\"\n}}\n"
        )
        os.chmod(KAGGLE_JSON, 0o600)


def download_model() -> Path | None:
    """Download model artifact from Kaggle dataset."""
    if not settings.kaggle_dataset or not settings.kaggle_model_file:
        return None

    ensure_kaggle_credentials()

    output_dir = MODELS_DIR / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use Kaggle CLI to download specific file from dataset
    cmd = [
        "kaggle", "datasets", "download",
        "-d", settings.kaggle_dataset,
        "-f", settings.kaggle_model_file,
        "-p", str(output_dir),
        "-o",
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as exc:
        # Fallback: ignore if not available in environment
        return None

    # Extract if zipped
    downloaded = output_dir / settings.kaggle_model_file
    if downloaded.suffix == ".zip":
        import zipfile
        with zipfile.ZipFile(downloaded, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        return next(output_dir.glob("*.joblib"), None)

    return downloaded if downloaded.exists() else None
