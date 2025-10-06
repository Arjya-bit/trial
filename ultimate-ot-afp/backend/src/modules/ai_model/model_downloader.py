"""
Kaggle Model Downloader for Ultimate OT-AFP Platform
"""

import os
import kaggle
import asyncio
import aiohttp
import zipfile
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import hashlib

from ...core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class ModelInfo:
    """Model information structure"""
    name: str
    kaggle_path: str
    model_type: str
    description: str
    input_format: str
    output_format: str
    local_path: Optional[str] = None
    downloaded: bool = False
    model_size: Optional[int] = None
    last_updated: Optional[str] = None

class KaggleModelDownloader:
    """Download and manage AI models from Kaggle"""
    
    def __init__(self):
        self.models_config = self._load_models_config()
        self.models_dir = Path(settings.AI_MODEL_PATH)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._setup_kaggle_credentials()
    
    def _load_models_config(self) -> Dict:
        """Load AI models configuration"""
        config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load models config: {e}")
            return {"cybersecurity_models": [], "forensics_models": [], "ot_security_models": []}
    
    def _setup_kaggle_credentials(self):
        """Setup Kaggle API credentials"""
        try:
            if settings.KAGGLE_USERNAME and settings.KAGGLE_KEY:
                os.environ['KAGGLE_USERNAME'] = settings.KAGGLE_USERNAME
                os.environ['KAGGLE_KEY'] = settings.KAGGLE_KEY
            
            # Verify credentials
            kaggle.api.authenticate()
            logger.info("✅ Kaggle API credentials configured")
            
        except Exception as e:
            logger.error(f"❌ Kaggle API setup failed: {e}")
            logger.info("Please set KAGGLE_USERNAME and KAGGLE_KEY in environment variables")
    
    def get_available_models(self) -> List[ModelInfo]:
        """Get list of available models"""
        models = []
        
        for category in ['cybersecurity_models', 'forensics_models', 'ot_security_models']:
            for model_config in self.models_config.get(category, []):
                model_info = ModelInfo(**model_config)
                
                # Check if model is already downloaded
                model_path = self.models_dir / model_info.name
                if model_path.exists():
                    model_info.local_path = str(model_path)
                    model_info.downloaded = True
                    
                    # Get model size
                    try:
                        model_info.model_size = sum(
                            f.stat().st_size for f in model_path.rglob('*') if f.is_file()
                        )
                    except Exception:
                        pass
                
                models.append(model_info)
        
        return models
    
    async def download_model(self, model_name: str, force_update: bool = False) -> bool:
        """Download a specific model from Kaggle"""
        try:
            # Find model configuration
            model_info = None
            for category in ['cybersecurity_models', 'forensics_models', 'ot_security_models']:
                for model_config in self.models_config.get(category, []):
                    if model_config['name'] == model_name:
                        model_info = ModelInfo(**model_config)
                        break
                if model_info:
                    break
            
            if not model_info:
                logger.error(f"Model '{model_name}' not found in configuration")
                return False
            
            model_dir = self.models_dir / model_name
            
            # Check if already downloaded
            if model_dir.exists() and not force_update:
                logger.info(f"Model '{model_name}' already exists. Use force_update=True to re-download")
                return True
            
            # Create model directory
            model_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"🔽 Downloading model: {model_name} from {model_info.kaggle_path}")
            
            # Download from Kaggle
            try:
                if "datasets" in model_info.kaggle_path:
                    # Download dataset
                    dataset_path = model_info.kaggle_path.replace("datasets/", "")
                    kaggle.api.dataset_download_files(
                        dataset_path,
                        path=str(model_dir),
                        unzip=True
                    )
                else:
                    # Download competition data or model
                    kaggle.api.competition_download_files(
                        model_info.kaggle_path,
                        path=str(model_dir)
                    )
                
                # Extract if needed
                for zip_file in model_dir.glob("*.zip"):
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(model_dir)
                    zip_file.unlink()  # Remove zip file
                
                logger.info(f"✅ Successfully downloaded model: {model_name}")
                
                # Save model metadata
                await self._save_model_metadata(model_name, model_info)
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to download from Kaggle: {e}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error downloading model '{model_name}': {e}")
            return False
    
    async def download_all_models(self, category: Optional[str] = None) -> Dict[str, bool]:
        """Download all models or models from a specific category"""
        results = {}
        
        categories = [category] if category else ['cybersecurity_models', 'forensics_models', 'ot_security_models']
        
        for cat in categories:
            for model_config in self.models_config.get(cat, []):
                model_name = model_config['name']
                logger.info(f"📥 Starting download for {model_name}")
                results[model_name] = await self.download_model(model_name)
        
        return results
    
    async def _save_model_metadata(self, model_name: str, model_info: ModelInfo):
        """Save model metadata"""
        metadata = {
            "name": model_info.name,
            "kaggle_path": model_info.kaggle_path,
            "model_type": model_info.model_type,
            "description": model_info.description,
            "input_format": model_info.input_format,
            "output_format": model_info.output_format,
            "downloaded_at": str(asyncio.get_event_loop().time()),
            "local_path": str(self.models_dir / model_name)
        }
        
        metadata_file = self.models_dir / model_name / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """Get local path for a model"""
        model_path = self.models_dir / model_name
        return model_path if model_path.exists() else None
    
    def is_model_available(self, model_name: str) -> bool:
        """Check if model is available locally"""
        return (self.models_dir / model_name).exists()
    
    async def update_model(self, model_name: str) -> bool:
        """Update a specific model"""
        return await self.download_model(model_name, force_update=True)
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Get detailed information about a model"""
        metadata_file = self.models_dir / model_name / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to read model metadata: {e}")
        return None
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a local model"""
        try:
            model_path = self.models_dir / model_name
            if model_path.exists():
                import shutil
                shutil.rmtree(model_path)
                logger.info(f"🗑️ Deleted model: {model_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete model '{model_name}': {e}")
            return False

# Global model downloader instance
model_downloader = KaggleModelDownloader()

# Utility functions
async def ensure_model_available(model_name: str) -> bool:
    """Ensure a model is available, download if necessary"""
    if model_downloader.is_model_available(model_name):
        return True
    
    logger.info(f"Model '{model_name}' not found locally. Downloading...")
    return await model_downloader.download_model(model_name)

async def get_best_model_for_task(task_type: str) -> Optional[str]:
    """Get the best model for a specific task type"""
    from .config import DEFAULT_MODELS
    
    model_name = DEFAULT_MODELS.get(task_type)
    if model_name and await ensure_model_available(model_name):
        return model_name
    return None