"""
AI Model Training Engine for Ultimate OT-AFP Platform
"""

import asyncio
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple
import logging
from pathlib import Path
import joblib
import json
from datetime import datetime
from dataclasses import dataclass

# ML libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from ...core.config import settings
from .model_downloader import model_downloader

logger = logging.getLogger(__name__)

@dataclass
class TrainingResult:
    """Result of model training"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    model_path: str
    metadata: Dict[str, Any]

class ModelTrainer:
    """AI Model Training Engine"""
    
    def __init__(self):
        self.models_dir = Path(settings.AI_MODEL_PATH)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"🏋️ Model Trainer initialized on {self.device}")
    
    async def train_malware_classifier(self, training_data: pd.DataFrame, 
                                     target_column: str = 'is_malware') -> TrainingResult:
        """Train malware classification model"""
        try:
            logger.info("🔬 Training malware classification model...")
            
            # Prepare data
            X = training_data.drop(columns=[target_column])
            y = training_data[target_column]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=10,
                min_samples_leaf=4,
                random_state=42,
                n_jobs=-1
            )
            
            import time
            start_time = time.time()
            model.fit(X_train_scaled, y_train)
            training_time = time.time() - start_time
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Save model
            model_name = "custom_malware_classifier"
            model_path = await self._save_sklearn_model(
                model, scaler, model_name, "malware_classification"
            )
            
            logger.info(f"✅ Malware classifier trained - Accuracy: {accuracy:.3f}")
            
            return TrainingResult(
                model_name=model_name,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                training_time=training_time,
                model_path=str(model_path),
                metadata={
                    "model_type": "malware_classification",
                    "features": list(X.columns),
                    "classes": list(np.unique(y))
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error training malware classifier: {e}")
            raise
    
    async def train_anomaly_detector(self, normal_data: pd.DataFrame, 
                                   contamination: float = 0.1) -> TrainingResult:
        """Train anomaly detection model"""
        try:
            logger.info("🔍 Training anomaly detection model...")
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(normal_data)
            
            # Train isolation forest
            model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_jobs=-1,
                n_estimators=200
            )
            
            import time
            start_time = time.time()
            model.fit(X_scaled)
            training_time = time.time() - start_time
            
            # Evaluate on training data (for anomaly detection)
            predictions = model.predict(X_scaled)
            anomaly_scores = model.decision_function(X_scaled)
            
            # Calculate metrics (assuming normal data should have low anomaly rate)
            normal_predictions = np.sum(predictions == 1)
            total_predictions = len(predictions)
            accuracy = normal_predictions / total_predictions
            
            # Save model
            model_name = "custom_anomaly_detector"
            model_path = await self._save_sklearn_model(
                model, scaler, model_name, "anomaly_detection"
            )
            
            logger.info(f"✅ Anomaly detector trained - Normal rate: {accuracy:.3f}")
            
            return TrainingResult(
                model_name=model_name,
                accuracy=accuracy,
                precision=accuracy,  # For anomaly detection
                recall=accuracy,
                f1_score=accuracy,
                training_time=training_time,
                model_path=str(model_path),
                metadata={
                    "model_type": "anomaly_detection",
                    "contamination": contamination,
                    "features": list(normal_data.columns)
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error training anomaly detector: {e}")
            raise
    
    async def train_network_classifier(self, network_data: pd.DataFrame, 
                                     target_column: str = 'attack_type') -> TrainingResult:
        """Train network intrusion classification model"""
        try:
            logger.info("🌐 Training network intrusion classifier...")
            
            # Prepare data
            X = network_data.drop(columns=[target_column])
            y = network_data[target_column]
            
            # Encode categorical variables
            label_encoders = {}
            for column in X.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                X[column] = le.fit_transform(X[column].astype(str))
                label_encoders[column] = le
            
            # Encode target variable
            target_encoder = LabelEncoder()
            y_encoded = target_encoder.fit_transform(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestClassifier(
                n_estimators=300,
                max_depth=25,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            import time
            start_time = time.time()
            model.fit(X_train_scaled, y_train)
            training_time = time.time() - start_time
            
            # Evaluate model
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Save model with encoders
            model_name = "custom_network_classifier"
            model_path = await self._save_sklearn_model(
                model, scaler, model_name, "network_classification",
                extra_artifacts={
                    'label_encoders': label_encoders,
                    'target_encoder': target_encoder
                }
            )
            
            logger.info(f"✅ Network classifier trained - Accuracy: {accuracy:.3f}")
            
            return TrainingResult(
                model_name=model_name,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                training_time=training_time,
                model_path=str(model_path),
                metadata={
                    "model_type": "network_classification",
                    "features": list(X.columns),
                    "classes": list(target_encoder.classes_)
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error training network classifier: {e}")
            raise
    
    async def train_pytorch_model(self, model_architecture: nn.Module, 
                                train_loader: DataLoader, 
                                val_loader: DataLoader,
                                model_name: str,
                                epochs: int = 50) -> TrainingResult:
        """Train PyTorch deep learning model"""
        try:
            logger.info(f"🚀 Training PyTorch model: {model_name}")
            
            model = model_architecture.to(self.device)
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)
            
            import time
            start_time = time.time()
            
            best_val_accuracy = 0.0
            train_losses = []
            val_accuracies = []
            
            for epoch in range(epochs):
                # Training
                model.train()
                train_loss = 0.0
                for batch_idx, (data, target) in enumerate(train_loader):
                    data, target = data.to(self.device), target.to(self.device)
                    
                    optimizer.zero_grad()
                    output = model(data)
                    loss = criterion(output, target)
                    loss.backward()
                    optimizer.step()
                    
                    train_loss += loss.item()
                
                # Validation
                model.eval()
                val_correct = 0
                val_total = 0
                val_loss = 0.0
                
                with torch.no_grad():
                    for data, target in val_loader:
                        data, target = data.to(self.device), target.to(self.device)
                        output = model(data)
                        val_loss += criterion(output, target).item()
                        
                        _, predicted = torch.max(output.data, 1)
                        val_total += target.size(0)
                        val_correct += (predicted == target).sum().item()
                
                val_accuracy = val_correct / val_total
                avg_train_loss = train_loss / len(train_loader)
                avg_val_loss = val_loss / len(val_loader)
                
                train_losses.append(avg_train_loss)
                val_accuracies.append(val_accuracy)
                
                scheduler.step(avg_val_loss)
                
                if val_accuracy > best_val_accuracy:
                    best_val_accuracy = val_accuracy
                
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Train Loss: {avg_train_loss:.4f}, "
                              f"Val Accuracy: {val_accuracy:.4f}")
            
            training_time = time.time() - start_time
            
            # Save PyTorch model
            model_path = await self._save_pytorch_model(model, model_name)
            
            logger.info(f"✅ PyTorch model trained - Best Val Accuracy: {best_val_accuracy:.3f}")
            
            return TrainingResult(
                model_name=model_name,
                accuracy=best_val_accuracy,
                precision=best_val_accuracy,  # Simplified for demo
                recall=best_val_accuracy,
                f1_score=best_val_accuracy,
                training_time=training_time,
                model_path=str(model_path),
                metadata={
                    "model_type": "deep_learning",
                    "architecture": str(model_architecture),
                    "epochs": epochs,
                    "train_losses": train_losses,
                    "val_accuracies": val_accuracies
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error training PyTorch model: {e}")
            raise
    
    async def _save_sklearn_model(self, model: Any, scaler: Any, 
                                model_name: str, model_type: str,
                                extra_artifacts: Dict = None) -> Path:
        """Save scikit-learn model with artifacts"""
        model_dir = self.models_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = model_dir / "model.pkl"
        joblib.dump(model, model_path)
        
        # Save scaler
        scaler_path = model_dir / "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        
        # Save extra artifacts
        if extra_artifacts:
            for name, artifact in extra_artifacts.items():
                artifact_path = model_dir / f"{name}.pkl"
                joblib.dump(artifact, artifact_path)
        
        # Save metadata
        metadata = {
            "name": model_name,
            "model_type": model_type,
            "framework": "scikit-learn",
            "created_at": datetime.now().isoformat(),
            "local_path": str(model_dir),
            "artifacts": ["model.pkl", "scaler.pkl"] + (list(extra_artifacts.keys()) if extra_artifacts else [])
        }
        
        metadata_path = model_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return model_dir
    
    async def _save_pytorch_model(self, model: nn.Module, model_name: str) -> Path:
        """Save PyTorch model"""
        model_dir = self.models_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model state dict
        model_path = model_dir / "model.pth"
        torch.save(model.state_dict(), model_path)
        
        # Save full model
        full_model_path = model_dir / "full_model.pth"
        torch.save(model, full_model_path)
        
        # Save metadata
        metadata = {
            "name": model_name,
            "model_type": "deep_learning",
            "framework": "pytorch",
            "created_at": datetime.now().isoformat(),
            "local_path": str(model_dir),
            "artifacts": ["model.pth", "full_model.pth"]
        }
        
        metadata_path = model_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return model_dir
    
    async def retrain_model(self, model_name: str, new_data: pd.DataFrame) -> TrainingResult:
        """Retrain an existing model with new data"""
        logger.info(f"🔄 Retraining model: {model_name}")
        
        # Load existing model metadata
        model_path = self.models_dir / model_name
        metadata_file = model_path / "metadata.json"
        
        if not metadata_file.exists():
            raise ValueError(f"Model {model_name} metadata not found")
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        model_type = metadata.get('model_type')
        
        # Retrain based on model type
        if model_type == "malware_classification":
            return await self.train_malware_classifier(new_data)
        elif model_type == "anomaly_detection":
            return await self.train_anomaly_detector(new_data)
        elif model_type == "network_classification":
            return await self.train_network_classifier(new_data)
        else:
            raise ValueError(f"Unsupported model type for retraining: {model_type}")
    
    def get_training_history(self, model_name: str) -> Optional[Dict]:
        """Get training history for a model"""
        metadata_file = self.models_dir / model_name / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return None

# Global model trainer instance
model_trainer = ModelTrainer()

# Utility functions
async def quick_train_malware_detector(file_features: pd.DataFrame) -> TrainingResult:
    """Quick training of malware detector"""
    return await model_trainer.train_malware_classifier(file_features)

async def quick_train_anomaly_detector(normal_traffic: pd.DataFrame) -> TrainingResult:
    """Quick training of anomaly detector"""
    return await model_trainer.train_anomaly_detector(normal_traffic)