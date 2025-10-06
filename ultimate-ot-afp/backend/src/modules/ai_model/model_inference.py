"""
AI Model Inference Engine for Ultimate OT-AFP Platform
"""

import asyncio
import torch
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Union, Tuple
import logging
from pathlib import Path
import joblib
import pickle
from dataclasses import dataclass
import json
import time

# ML libraries
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from transformers import AutoTokenizer, AutoModel, pipeline
import tensorflow as tf

from ...core.config import settings
from .model_downloader import model_downloader, get_best_model_for_task

logger = logging.getLogger(__name__)

@dataclass
class InferenceResult:
    """Result of model inference"""
    prediction: Any
    confidence: float
    model_name: str
    inference_time: float
    metadata: Dict[str, Any]

class ModelInferenceEngine:
    """Advanced AI model inference engine"""
    
    def __init__(self):
        self.loaded_models = {}
        self.model_metadata = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"🧠 AI Inference Engine initialized on {self.device}")
    
    async def load_model(self, model_name: str) -> bool:
        """Load a model into memory"""
        try:
            if model_name in self.loaded_models:
                logger.info(f"Model '{model_name}' already loaded")
                return True
            
            model_path = model_downloader.get_model_path(model_name)
            if not model_path:
                logger.error(f"Model '{model_name}' not found locally")
                return False
            
            # Load model metadata
            metadata_file = model_path / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    self.model_metadata[model_name] = json.load(f)
            
            model_type = self.model_metadata.get(model_name, {}).get('model_type', 'unknown')
            
            # Load model based on type
            if model_type == 'classification':
                model = await self._load_classification_model(model_path)
            elif model_type == 'anomaly_detection':
                model = await self._load_anomaly_model(model_path)
            elif model_type == 'nlp_anomaly':
                model = await self._load_nlp_model(model_path)
            elif model_type == 'image_analysis':
                model = await self._load_image_model(model_path)
            elif model_type == 'time_series_anomaly':
                model = await self._load_timeseries_model(model_path)
            elif model_type == 'protocol_analysis':
                model = await self._load_protocol_model(model_path)
            else:
                model = await self._load_generic_model(model_path)
            
            if model:
                self.loaded_models[model_name] = model
                logger.info(f"✅ Successfully loaded model: {model_name}")
                return True
            else:
                logger.error(f"❌ Failed to load model: {model_name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading model '{model_name}': {e}")
            return False
    
    async def _load_classification_model(self, model_path: Path) -> Any:
        """Load classification model"""
        try:
            # Look for scikit-learn models
            for model_file in model_path.glob("*.pkl"):
                return joblib.load(model_file)
            
            # Look for PyTorch models
            for model_file in model_path.glob("*.pth"):
                return torch.load(model_file, map_location=self.device)
            
            # Look for TensorFlow models
            tf_model_dir = model_path / "saved_model"
            if tf_model_dir.exists():
                return tf.keras.models.load_model(str(tf_model_dir))
            
            # Create a default model if no pre-trained model found
            logger.warning(f"No pre-trained model found in {model_path}, creating default classifier")
            return self._create_default_classifier()
            
        except Exception as e:
            logger.error(f"Error loading classification model: {e}")
            return None
    
    async def _load_anomaly_model(self, model_path: Path) -> Any:
        """Load anomaly detection model"""
        try:
            # Look for existing anomaly detection models
            for model_file in model_path.glob("*.pkl"):
                return joblib.load(model_file)
            
            # Create default Isolation Forest
            logger.warning(f"No pre-trained anomaly model found, creating default Isolation Forest")
            return IsolationForest(contamination=0.1, random_state=42)
            
        except Exception as e:
            logger.error(f"Error loading anomaly model: {e}")
            return None
    
    async def _load_nlp_model(self, model_path: Path) -> Any:
        """Load NLP model for log analysis"""
        try:
            # Try to load Hugging Face transformers model
            if (model_path / "config.json").exists():
                tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                model = AutoModel.from_pretrained(str(model_path))
                return {"tokenizer": tokenizer, "model": model}
            
            # Create default NLP pipeline
            logger.warning("Creating default NLP pipeline")
            return pipeline("text-classification", model="distilbert-base-uncased")
            
        except Exception as e:
            logger.error(f"Error loading NLP model: {e}")
            return None
    
    async def _load_image_model(self, model_path: Path) -> Any:
        """Load image analysis model"""
        try:
            # Look for TensorFlow/Keras models
            if (model_path / "saved_model").exists():
                return tf.keras.models.load_model(str(model_path / "saved_model"))
            
            # Look for PyTorch models
            for model_file in model_path.glob("*.pth"):
                return torch.load(model_file, map_location=self.device)
            
            # Create default image classifier
            logger.warning("Creating default image model")
            return pipeline("image-classification")
            
        except Exception as e:
            logger.error(f"Error loading image model: {e}")
            return None
    
    async def _load_timeseries_model(self, model_path: Path) -> Any:
        """Load time series anomaly detection model"""
        try:
            # Look for scikit-learn models
            for model_file in model_path.glob("*.pkl"):
                return joblib.load(model_file)
            
            # Create default time series anomaly detector
            logger.warning("Creating default time series anomaly detector")
            return IsolationForest(contamination=0.05, random_state=42)
            
        except Exception as e:
            logger.error(f"Error loading time series model: {e}")
            return None
    
    async def _load_protocol_model(self, model_path: Path) -> Any:
        """Load protocol analysis model"""
        try:
            # Look for existing models
            for model_file in model_path.glob("*.pkl"):
                return joblib.load(model_file)
            
            # Create default protocol classifier
            logger.warning("Creating default protocol analyzer")
            return RandomForestClassifier(n_estimators=100, random_state=42)
            
        except Exception as e:
            logger.error(f"Error loading protocol model: {e}")
            return None
    
    async def _load_generic_model(self, model_path: Path) -> Any:
        """Load generic model"""
        try:
            # Try different model formats
            for model_file in model_path.glob("*.pkl"):
                return joblib.load(model_file)
            
            for model_file in model_path.glob("*.pth"):
                return torch.load(model_file, map_location=self.device)
            
            # Default fallback
            return RandomForestClassifier(n_estimators=50, random_state=42)
            
        except Exception as e:
            logger.error(f"Error loading generic model: {e}")
            return None
    
    def _create_default_classifier(self) -> Any:
        """Create a default classifier"""
        return RandomForestClassifier(n_estimators=100, random_state=42)
    
    async def predict(self, model_name: str, data: Any, **kwargs) -> InferenceResult:
        """Make prediction using specified model"""
        start_time = time.time()
        
        try:
            # Ensure model is loaded
            if model_name not in self.loaded_models:
                await self.load_model(model_name)
            
            if model_name not in self.loaded_models:
                raise ValueError(f"Model '{model_name}' could not be loaded")
            
            model = self.loaded_models[model_name]
            model_type = self.model_metadata.get(model_name, {}).get('model_type', 'unknown')
            
            # Make prediction based on model type
            if model_type == 'classification':
                prediction, confidence = await self._predict_classification(model, data)
            elif model_type == 'anomaly_detection':
                prediction, confidence = await self._predict_anomaly(model, data)
            elif model_type == 'nlp_anomaly':
                prediction, confidence = await self._predict_nlp(model, data)
            elif model_type == 'image_analysis':
                prediction, confidence = await self._predict_image(model, data)
            elif model_type == 'time_series_anomaly':
                prediction, confidence = await self._predict_timeseries(model, data)
            elif model_type == 'protocol_analysis':
                prediction, confidence = await self._predict_protocol(model, data)
            else:
                prediction, confidence = await self._predict_generic(model, data)
            
            inference_time = time.time() - start_time
            
            return InferenceResult(
                prediction=prediction,
                confidence=confidence,
                model_name=model_name,
                inference_time=inference_time,
                metadata=self.model_metadata.get(model_name, {})
            )
            
        except Exception as e:
            logger.error(f"❌ Prediction error with model '{model_name}': {e}")
            inference_time = time.time() - start_time
            return InferenceResult(
                prediction=None,
                confidence=0.0,
                model_name=model_name,
                inference_time=inference_time,
                metadata={"error": str(e)}
            )
    
    async def _predict_classification(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Classification prediction"""
        try:
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(data)
                prediction = model.predict(data)
                confidence = float(np.max(probabilities))
            else:
                prediction = model.predict(data)
                confidence = 0.8  # Default confidence
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Classification prediction error: {e}")
            return None, 0.0
    
    async def _predict_anomaly(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Anomaly detection prediction"""
        try:
            prediction = model.predict(data)
            anomaly_score = model.decision_function(data)
            confidence = float(np.abs(np.mean(anomaly_score)))
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Anomaly prediction error: {e}")
            return None, 0.0
    
    async def _predict_nlp(self, model: Any, data: Any) -> Tuple[Any, float]:
        """NLP prediction"""
        try:
            if isinstance(model, dict) and "tokenizer" in model:
                # Hugging Face model
                tokenizer = model["tokenizer"]
                nlp_model = model["model"]
                inputs = tokenizer(data, return_tensors="pt", truncation=True, padding=True)
                outputs = nlp_model(**inputs)
                prediction = outputs.last_hidden_state.mean(dim=1).detach().numpy()
                confidence = 0.75
            else:
                # Pipeline model
                result = model(data)
                prediction = result[0]['label'] if isinstance(result, list) else result
                confidence = result[0]['score'] if isinstance(result, list) else 0.75
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"NLP prediction error: {e}")
            return None, 0.0
    
    async def _predict_image(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Image analysis prediction"""
        try:
            if hasattr(model, '__call__'):  # Pipeline model
                result = model(data)
                prediction = result[0]['label'] if isinstance(result, list) else result
                confidence = result[0]['score'] if isinstance(result, list) else 0.75
            else:
                # TensorFlow/PyTorch model
                prediction = model.predict(data)
                confidence = float(np.max(prediction))
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Image prediction error: {e}")
            return None, 0.0
    
    async def _predict_timeseries(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Time series prediction"""
        try:
            prediction = model.predict(data)
            if hasattr(model, 'decision_function'):
                anomaly_score = model.decision_function(data)
                confidence = float(np.abs(np.mean(anomaly_score)))
            else:
                confidence = 0.8
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Time series prediction error: {e}")
            return None, 0.0
    
    async def _predict_protocol(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Protocol analysis prediction"""
        try:
            prediction = model.predict(data)
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(data)
                confidence = float(np.max(probabilities))
            else:
                confidence = 0.8
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Protocol prediction error: {e}")
            return None, 0.0
    
    async def _predict_generic(self, model: Any, data: Any) -> Tuple[Any, float]:
        """Generic prediction"""
        try:
            prediction = model.predict(data)
            confidence = 0.75  # Default confidence
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Generic prediction error: {e}")
            return None, 0.0
    
    def unload_model(self, model_name: str):
        """Unload model from memory"""
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            logger.info(f"🗑️ Unloaded model: {model_name}")
    
    def get_loaded_models(self) -> List[str]:
        """Get list of loaded models"""
        return list(self.loaded_models.keys())
    
    async def batch_predict(self, model_name: str, data_batch: List[Any]) -> List[InferenceResult]:
        """Make batch predictions"""
        results = []
        for data in data_batch:
            result = await self.predict(model_name, data)
            results.append(result)
        return results

# Global inference engine instance
inference_engine = ModelInferenceEngine()

# Utility functions for common AI tasks
async def analyze_malware(file_data: bytes) -> InferenceResult:
    """Analyze file for malware"""
    model_name = await get_best_model_for_task("malware_detection")
    if model_name:
        return await inference_engine.predict(model_name, file_data)
    return InferenceResult(None, 0.0, "none", 0.0, {"error": "No model available"})

async def detect_network_intrusion(network_data: Dict) -> InferenceResult:
    """Detect network intrusions"""
    model_name = await get_best_model_for_task("intrusion_detection")
    if model_name:
        return await inference_engine.predict(model_name, network_data)
    return InferenceResult(None, 0.0, "none", 0.0, {"error": "No model available"})

async def analyze_logs(log_entries: List[str]) -> InferenceResult:
    """Analyze system logs for anomalies"""
    model_name = await get_best_model_for_task("log_analysis")
    if model_name:
        return await inference_engine.predict(model_name, log_entries)
    return InferenceResult(None, 0.0, "none", 0.0, {"error": "No model available"})