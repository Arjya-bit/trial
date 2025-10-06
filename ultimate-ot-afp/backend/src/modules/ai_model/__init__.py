"""
AI Model module initialization
"""

from .model_downloader import model_downloader, ensure_model_available, get_best_model_for_task
from .model_inference import inference_engine, analyze_malware, detect_network_intrusion, analyze_logs
from .model_trainer import model_trainer, quick_train_malware_detector, quick_train_anomaly_detector

__all__ = [
    "model_downloader",
    "inference_engine", 
    "model_trainer",
    "ensure_model_available",
    "get_best_model_for_task",
    "analyze_malware",
    "detect_network_intrusion", 
    "analyze_logs",
    "quick_train_malware_detector",
    "quick_train_anomaly_detector"
]