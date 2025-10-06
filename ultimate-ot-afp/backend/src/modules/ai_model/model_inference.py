"""
AI Model Inference Engine
Performs inference on loaded AI models for cybersecurity analysis
"""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import pickle
import joblib

logger = logging.getLogger(__name__)


class AIModelInference:
    """AI Model Inference for Cybersecurity Analysis"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = []
        
    def load_model(self, model_file: str = "model.pkl"):
        """Load a trained model"""
        try:
            model_filepath = self.model_path / model_file
            
            if model_filepath.suffix == '.pkl':
                with open(model_filepath, 'rb') as f:
                    self.model = pickle.load(f)
            elif model_filepath.suffix == '.joblib':
                self.model = joblib.load(model_filepath)
            else:
                raise ValueError(f"Unsupported model format: {model_filepath.suffix}")
            
            logger.info(f"Model loaded from: {model_filepath}")
            
            # Try to load associated preprocessing objects
            self._load_preprocessing_objects()
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _load_preprocessing_objects(self):
        """Load preprocessing objects (scaler, encoder)"""
        try:
            scaler_path = self.model_path / "scaler.pkl"
            if scaler_path.exists():
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                logger.info("Scaler loaded")
            
            encoder_path = self.model_path / "label_encoder.pkl"
            if encoder_path.exists():
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                logger.info("Label encoder loaded")
            
            features_path = self.model_path / "feature_names.txt"
            if features_path.exists():
                with open(features_path, 'r') as f:
                    self.feature_names = [line.strip() for line in f]
                logger.info(f"Feature names loaded: {len(self.feature_names)} features")
                
        except Exception as e:
            logger.warning(f"Could not load preprocessing objects: {e}")
    
    def preprocess_input(self, data: Dict[str, Any]) -> np.ndarray:
        """Preprocess input data for inference"""
        try:
            # Convert dict to DataFrame
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                df = pd.DataFrame(data)
            
            # Ensure correct feature order
            if self.feature_names:
                missing_features = set(self.feature_names) - set(df.columns)
                if missing_features:
                    logger.warning(f"Missing features: {missing_features}")
                    for feature in missing_features:
                        df[feature] = 0
                
                df = df[self.feature_names]
            
            # Apply scaling if available
            if self.scaler:
                X = self.scaler.transform(df)
            else:
                X = df.values
            
            return X
            
        except Exception as e:
            logger.error(f"Error preprocessing input: {e}")
            raise
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction on input data
        
        Args:
            data: Input features as dict
            
        Returns:
            Prediction results with confidence scores
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            X = self.preprocess_input(data)
            
            # Get prediction
            prediction = self.model.predict(X)[0]
            
            # Get probability if available
            probabilities = None
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(X)[0]
            
            # Decode label if encoder available
            if self.label_encoder:
                prediction_label = self.label_encoder.inverse_transform([prediction])[0]
            else:
                prediction_label = str(prediction)
            
            result = {
                "prediction": prediction_label,
                "prediction_raw": int(prediction),
                "confidence": float(max(probabilities)) if probabilities is not None else None,
                "probabilities": probabilities.tolist() if probabilities is not None else None
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make predictions on batch of data"""
        return [self.predict(data) for data in data_list]
    
    def analyze_network_traffic(self, packet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze network traffic for anomalies and threats
        
        Args:
            packet_data: Network packet features
            
        Returns:
            Analysis results including threat classification
        """
        try:
            prediction = self.predict(packet_data)
            
            # Add threat analysis
            is_malicious = prediction['prediction'] in ['attack', 'malicious', 'anomaly', '1']
            
            result = {
                **prediction,
                "is_malicious": is_malicious,
                "threat_level": self._calculate_threat_level(prediction),
                "recommended_action": self._get_recommended_action(prediction)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing network traffic: {e}")
            raise
    
    def analyze_malware(self, malware_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze malware characteristics
        
        Args:
            malware_features: Malware behavioral features
            
        Returns:
            Malware classification and characteristics
        """
        try:
            prediction = self.predict(malware_features)
            
            result = {
                **prediction,
                "malware_family": prediction['prediction'],
                "severity": self._calculate_threat_level(prediction),
                "indicators": self._extract_indicators(malware_features)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing malware: {e}")
            raise
    
    def _calculate_threat_level(self, prediction: Dict[str, Any]) -> str:
        """Calculate threat level from prediction"""
        confidence = prediction.get('confidence', 0)
        
        if confidence >= 0.9:
            return "critical"
        elif confidence >= 0.7:
            return "high"
        elif confidence >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _get_recommended_action(self, prediction: Dict[str, Any]) -> str:
        """Get recommended action based on prediction"""
        threat_level = self._calculate_threat_level(prediction)
        
        actions = {
            "critical": "Block immediately and escalate to security team",
            "high": "Block and investigate",
            "medium": "Monitor closely and log",
            "low": "Log for analysis"
        }
        
        return actions.get(threat_level, "Monitor")
    
    def _extract_indicators(self, features: Dict[str, Any]) -> List[str]:
        """Extract indicators of compromise from features"""
        indicators = []
        
        # This is a placeholder - implement based on your feature set
        for key, value in features.items():
            if isinstance(value, (int, float)) and value > 0:
                indicators.append(f"{key}: {value}")
        
        return indicators[:10]  # Return top 10 indicators


# Global inference instance
_inference_instance: Optional[AIModelInference] = None


def get_inference_engine() -> AIModelInference:
    """Get or create global inference engine instance"""
    global _inference_instance
    
    if _inference_instance is None:
        _inference_instance = AIModelInference()
    
    return _inference_instance
