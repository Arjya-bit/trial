"""
AI Model Trainer
Train and fine-tune AI models on cybersecurity data
"""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import joblib
import logging

logger = logging.getLogger(__name__)


class AIModelTrainer:
    """Train AI models for cybersecurity analysis"""
    
    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = []
        self.training_history = {}
    
    def load_data(self, data_path: str, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load training data from CSV
        
        Args:
            data_path: Path to CSV file
            target_column: Name of target column
            
        Returns:
            Features DataFrame and target Series
        """
        try:
            df = pd.read_csv(data_path)
            
            # Separate features and target
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            self.feature_names = X.columns.tolist()
            
            logger.info(f"Data loaded: {X.shape[0]} samples, {X.shape[1]} features")
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def preprocess_data(self, X: pd.DataFrame, y: pd.Series, fit: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess training data
        
        Args:
            X: Features DataFrame
            y: Target Series
            fit: Whether to fit preprocessing objects
            
        Returns:
            Preprocessed features and labels
        """
        try:
            # Handle categorical features
            X_processed = X.copy()
            
            # Encode categorical columns
            for col in X_processed.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                X_processed[col] = le.fit_transform(X_processed[col].astype(str))
            
            # Scale features
            if fit:
                self.scaler = StandardScaler()
                X_scaled = self.scaler.fit_transform(X_processed)
            else:
                X_scaled = self.scaler.transform(X_processed)
            
            # Encode target labels
            if fit:
                self.label_encoder = LabelEncoder()
                y_encoded = self.label_encoder.fit_transform(y)
            else:
                y_encoded = self.label_encoder.transform(y)
            
            logger.info("Data preprocessing completed")
            
            return X_scaled, y_encoded
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            raise
    
    def train_model(
        self,
        X: np.ndarray,
        y: np.ndarray,
        model_type: str = "random_forest",
        test_size: float = 0.2,
        **model_params
    ) -> Dict[str, Any]:
        """
        Train a machine learning model
        
        Args:
            X: Features array
            y: Target array
            model_type: Type of model ('random_forest', 'gradient_boost')
            test_size: Test set size
            **model_params: Additional model parameters
            
        Returns:
            Training metrics
        """
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            logger.info(f"Training set: {X_train.shape[0]} samples")
            logger.info(f"Test set: {X_test.shape[0]} samples")
            
            # Select model
            if model_type == "random_forest":
                self.model = RandomForestClassifier(
                    n_estimators=model_params.get('n_estimators', 100),
                    max_depth=model_params.get('max_depth', None),
                    random_state=42,
                    n_jobs=-1
                )
            elif model_type == "gradient_boost":
                self.model = GradientBoostingClassifier(
                    n_estimators=model_params.get('n_estimators', 100),
                    max_depth=model_params.get('max_depth', 5),
                    random_state=42
                )
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # Train model
            logger.info(f"Training {model_type} model...")
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            
            metrics = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "classification_report": classification_report(
                    y_test, y_pred,
                    target_names=self.label_encoder.classes_,
                    output_dict=True
                ),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
                "model_type": model_type,
                "n_features": X.shape[1],
                "n_samples": X.shape[0]
            }
            
            self.training_history = metrics
            
            logger.info(f"Model trained successfully. Accuracy: {metrics['accuracy']:.4f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def save_model(self, model_name: str = "model"):
        """Save trained model and preprocessing objects"""
        try:
            if self.model is None:
                raise ValueError("No trained model to save")
            
            # Save model
            model_file = self.model_path / f"{model_name}.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(self.model, f)
            logger.info(f"Model saved: {model_file}")
            
            # Save scaler
            if self.scaler:
                scaler_file = self.model_path / "scaler.pkl"
                with open(scaler_file, 'wb') as f:
                    pickle.dump(self.scaler, f)
                logger.info(f"Scaler saved: {scaler_file}")
            
            # Save label encoder
            if self.label_encoder:
                encoder_file = self.model_path / "label_encoder.pkl"
                with open(encoder_file, 'wb') as f:
                    pickle.dump(self.label_encoder, f)
                logger.info(f"Label encoder saved: {encoder_file}")
            
            # Save feature names
            if self.feature_names:
                features_file = self.model_path / "feature_names.txt"
                with open(features_file, 'w') as f:
                    f.write('\n'.join(self.feature_names))
                logger.info(f"Feature names saved: {features_file}")
            
            # Save training history
            history_file = self.model_path / "training_history.pkl"
            with open(history_file, 'wb') as f:
                pickle.dump(self.training_history, f)
            logger.info(f"Training history saved: {history_file}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def train_from_file(
        self,
        data_path: str,
        target_column: str,
        model_type: str = "random_forest",
        save: bool = True,
        **model_params
    ) -> Dict[str, Any]:
        """
        Complete training pipeline from file
        
        Args:
            data_path: Path to training data CSV
            target_column: Name of target column
            model_type: Type of model to train
            save: Whether to save trained model
            **model_params: Additional model parameters
            
        Returns:
            Training metrics
        """
        # Load data
        X, y = self.load_data(data_path, target_column)
        
        # Preprocess
        X_processed, y_processed = self.preprocess_data(X, y, fit=True)
        
        # Train
        metrics = self.train_model(X_processed, y_processed, model_type, **model_params)
        
        # Save
        if save:
            self.save_model()
        
        return metrics
