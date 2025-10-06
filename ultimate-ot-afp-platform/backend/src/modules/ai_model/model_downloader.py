"""
AI Model Downloader for Kaggle Integration
Downloads and manages AI models for forensics analysis
"""

import os
import json
import asyncio
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

logger = logging.getLogger(__name__)


class ModelDownloader:
    """Downloads and manages AI models from Kaggle"""

    def __init__(self):
        self.models_dir = Path("/app/models")
        self.config_file = self.models_dir / "models_config.json"
        self.api = KaggleApi()

        # Define available models for forensics analysis
        self.available_models = {
            "malware_detection": {
                "kaggle_dataset": "promptcloud/malware-analysis-datasets-top1000-pe-headers",
                "model_type": "classification",
                "description": "Dataset for malware analysis using PE headers"
            },
            "network_anomaly": {
                "kaggle_dataset": "mryanm/iot-intrusion-detection",
                "model_type": "anomaly_detection",
                "description": "IoT intrusion detection dataset"
            },
            "image_forensics": {
                "kaggle_dataset": "ciplab/real-and-fake-face-detection",
                "model_type": "image_classification",
                "description": "Real and fake face detection for digital forensics"
            },
            "text_analysis": {
                "kaggle_dataset": "rtatman/glove-global-vectors-for-word-representation",
                "model_type": "nlp_embeddings",
                "description": "GloVe word embeddings for text analysis"
            },
            "log_analysis": {
                "kaggle_dataset": "osmihelp/osmi-mental-health-in-tech-survey-2016",
                "model_type": "log_classification",
                "description": "Dataset for log analysis and anomaly detection"
            }
        }

        # Create models directory
        self.models_dir.mkdir(exist_ok=True)

    def authenticate_kaggle(self):
        """Authenticate with Kaggle API"""
        try:
            # Check if Kaggle credentials are configured
            kaggle_username = os.getenv('KAGGLE_USERNAME')
            kaggle_key = os.getenv('KAGGLE_KEY')

            if not kaggle_username or not kaggle_key:
                logger.warning("Kaggle credentials not found in environment variables")
                return False

            # Set up Kaggle API authentication
            os.environ['KAGGLE_USERNAME'] = kaggle_username
            os.environ['KAGGLE_KEY'] = kaggle_key

            # Authenticate
            self.api.authenticate()
            logger.info("Successfully authenticated with Kaggle API")
            return True

        except Exception as e:
            logger.error(f"Failed to authenticate with Kaggle: {e}")
            return False

    async def download_model(self, model_name: str) -> bool:
        """
        Download a specific model from Kaggle

        Args:
            model_name: Name of the model to download

        Returns:
            bool: True if successful, False otherwise
        """
        if model_name not in self.available_models:
            logger.error(f"Model '{model_name}' not found in available models")
            return False

        model_info = self.available_models[model_name]

        try:
            logger.info(f"Starting download for model: {model_name}")

            # Create model-specific directory
            model_dir = self.models_dir / model_name
            model_dir.mkdir(exist_ok=True)

            # Download dataset
            dataset_path = model_info["kaggle_dataset"]

            # Use kaggle CLI to download
            cmd = f"kaggle datasets download -d {dataset_path} -p {model_dir} --unzip"

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(model_dir)
            )

            if result.returncode == 0:
                logger.info(f"Successfully downloaded model: {model_name}")

                # Update model configuration
                await self.update_model_config(model_name, {
                    "status": "downloaded",
                    "path": str(model_dir),
                    "kaggle_dataset": dataset_path,
                    "download_date": asyncio.get_event_loop().time()
                })

                return True
            else:
                logger.error(f"Failed to download model {model_name}: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error downloading model {model_name}: {e}")
            return False

    async def download_all_models(self) -> Dict[str, bool]:
        """
        Download all available models

        Returns:
            Dict[str, bool]: Dictionary of model names and their download status
        """
        results = {}

        for model_name in self.available_models.keys():
            logger.info(f"Downloading model: {model_name}")
            results[model_name] = await self.download_model(model_name)

        return results

    async def update_model_config(self, model_name: str, config: Dict):
        """Update model configuration in the config file"""
        try:
            # Load existing config
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    models_config = json.load(f)
            else:
                models_config = {}

            # Update specific model config
            if model_name not in models_config:
                models_config[model_name] = {}

            models_config[model_name].update(config)

            # Save updated config
            with open(self.config_file, 'w') as f:
                json.dump(models_config, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating model config: {e}")

    async def get_model_config(self) -> Dict:
        """Get current model configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error reading model config: {e}")
            return {}

    async def initialize_models(self):
        """Initialize and download required models"""
        logger.info("Initializing AI models...")

        # Authenticate with Kaggle
        if not self.authenticate_kaggle():
            logger.warning("Kaggle authentication failed, models may not be available")

        # Check which models need to be downloaded
        config = await self.get_model_config()
        models_to_download = []

        for model_name, model_info in self.available_models.items():
            if model_name not in config or config[model_name].get("status") != "downloaded":
                models_to_download.append(model_name)

        if models_to_download:
            logger.info(f"Downloading {len(models_to_download)} models...")
            results = await self.download_all_models()

            successful = sum(1 for success in results.values() if success)
            logger.info(f"Downloaded {successful}/{len(models_to_download)} models successfully")
        else:
            logger.info("All models are already downloaded")

    def list_available_models(self) -> Dict:
        """List all available models and their status"""
        return self.available_models.copy()

    async def get_model_status(self, model_name: str) -> Dict:
        """Get status of a specific model"""
        config = await self.get_model_config()

        if model_name in config:
            return config[model_name]

        return {
            "status": "not_downloaded",
            "available": model_name in self.available_models
        }