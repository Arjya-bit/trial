"""
AI Model Downloader from Kaggle
Downloads and manages AI models for cybersecurity analysis
"""
import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class KaggleModelDownloader:
    """Download and manage AI models from Kaggle"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.config_path = self.model_path / "config.json"
        
    def setup_kaggle_credentials(self, username: str, key: str):
        """Setup Kaggle API credentials"""
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_dir.mkdir(exist_ok=True)
        
        kaggle_json = kaggle_dir / "kaggle.json"
        credentials = {
            "username": username,
            "key": key
        }
        
        with open(kaggle_json, 'w') as f:
            json.dump(credentials, f)
        
        # Set proper permissions (Unix only)
        if os.name != 'nt':
            os.chmod(kaggle_json, 0o600)
        
        logger.info("Kaggle credentials configured")
    
    async def download_dataset(self, dataset: str, force: bool = False) -> Path:
        """
        Download a Kaggle dataset
        
        Args:
            dataset: Dataset identifier (e.g., 'lakshmi25npathi/cybersecurity-incidents')
            force: Force re-download even if exists
            
        Returns:
            Path to downloaded dataset
        """
        try:
            import kaggle
            
            dataset_path = self.model_path / dataset.split('/')[-1]
            
            if dataset_path.exists() and not force:
                logger.info(f"Dataset already exists: {dataset_path}")
                return dataset_path
            
            logger.info(f"Downloading dataset: {dataset}")
            
            # Download using Kaggle API
            await asyncio.to_thread(
                kaggle.api.dataset_download_files,
                dataset,
                path=str(dataset_path),
                unzip=True
            )
            
            logger.info(f"Dataset downloaded to: {dataset_path}")
            return dataset_path
            
        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            raise
    
    async def download_model(self, model_name: str, owner: str = None) -> Path:
        """
        Download a pre-trained model from Kaggle
        
        Supported models for cybersecurity:
        - Intrusion Detection models
        - Malware Classification models
        - Anomaly Detection models
        - Network Traffic Analysis models
        """
        try:
            import kaggle
            
            model_path = self.model_path / model_name
            model_path.mkdir(parents=True, exist_ok=True)
            
            if owner:
                full_name = f"{owner}/{model_name}"
            else:
                full_name = model_name
            
            logger.info(f"Downloading model: {full_name}")
            
            # Note: Kaggle models API might be different based on model type
            # This is a general approach
            await asyncio.to_thread(
                kaggle.api.model_instance_get,
                full_name,
                str(model_path)
            )
            
            logger.info(f"Model downloaded to: {model_path}")
            return model_path
            
        except Exception as e:
            logger.error(f"Error downloading model: {e}")
            raise
    
    def save_model_config(self, config: Dict):
        """Save model configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Model config saved: {self.config_path}")
    
    def load_model_config(self) -> Optional[Dict]:
        """Load model configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return None


# Convenience functions
async def download_kaggle_model(
    dataset_name: str,
    username: str = None,
    api_key: str = None,
    model_path: str = "./models"
) -> Path:
    """
    Download a cybersecurity AI model from Kaggle
    
    Recommended datasets:
    - lakshmi25npathi/cybersecurity-incidents
    - cdc/cybersecurity-breaches
    - Cornell-University/malware-detection
    """
    downloader = KaggleModelDownloader(model_path)
    
    if username and api_key:
        downloader.setup_kaggle_credentials(username, api_key)
    
    dataset_path = await downloader.download_dataset(dataset_name)
    
    # Save configuration
    config = {
        "dataset": dataset_name,
        "path": str(dataset_path),
        "downloaded_at": str(Path.cwd())
    }
    downloader.save_model_config(config)
    
    return dataset_path


def setup_kaggle_credentials(username: str, api_key: str):
    """Setup Kaggle API credentials"""
    downloader = KaggleModelDownloader()
    downloader.setup_kaggle_credentials(username, api_key)


# Pre-configured cybersecurity models
CYBERSECURITY_MODELS = {
    "intrusion_detection": {
        "dataset": "sampadab17/network-intrusion-detection",
        "type": "classification",
        "description": "Network intrusion detection using ML"
    },
    "malware_detection": {
        "dataset": "Cornell-University/malware-detection",
        "type": "classification",
        "description": "Malware detection and classification"
    },
    "network_traffic": {
        "dataset": "jsrojas/ip-network-traffic-flows-labeled-with-87-apps",
        "type": "classification",
        "description": "Network traffic classification"
    },
    "cybersecurity_incidents": {
        "dataset": "lakshmi25npathi/cybersecurity-incidents",
        "type": "analysis",
        "description": "Cybersecurity incident data for analysis"
    },
    "phishing_detection": {
        "dataset": "shashwatwork/web-page-phishing-detection-dataset",
        "type": "classification",
        "description": "Phishing website detection"
    }
}


async def download_recommended_model(model_key: str = "cybersecurity_incidents") -> Path:
    """Download a recommended cybersecurity model"""
    if model_key not in CYBERSECURITY_MODELS:
        raise ValueError(f"Unknown model: {model_key}. Available: {list(CYBERSECURITY_MODELS.keys())}")
    
    model_info = CYBERSECURITY_MODELS[model_key]
    return await download_kaggle_model(model_info["dataset"])
