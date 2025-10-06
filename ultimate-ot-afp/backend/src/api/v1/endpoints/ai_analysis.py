"""
AI Analysis API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Dict, Any, Optional
import logging

from ...modules.ai_model import (
    model_downloader, inference_engine, model_trainer,
    analyze_malware, detect_network_intrusion, analyze_logs
)
from ...core.security import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/models")
async def list_available_models(current_user = Depends(get_current_user)):
    """List all available AI models"""
    try:
        models = model_downloader.get_available_models()
        return {
            "status": "success",
            "models": [
                {
                    "name": model.name,
                    "model_type": model.model_type,
                    "description": model.description,
                    "downloaded": model.downloaded,
                    "local_path": model.local_path,
                    "model_size": model.model_size
                } for model in models
            ]
        }
    except Exception as e:
        logger.error(f"❌ Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_name}/download")
async def download_model(model_name: str, force_update: bool = False, current_user = Depends(get_current_user)):
    """Download AI model from Kaggle"""
    try:
        success = await model_downloader.download_model(model_name, force_update)
        if success:
            return {"status": "success", "message": f"Model {model_name} downloaded successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to download model {model_name}")
    except Exception as e:
        logger.error(f"❌ Model download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/download-all")
async def download_all_models(category: Optional[str] = None, current_user = Depends(get_current_user)):
    """Download all AI models or models from specific category"""
    try:
        results = await model_downloader.download_all_models(category)
        return {
            "status": "success",
            "results": results,
            "total_models": len(results),
            "successful_downloads": sum(1 for success in results.values() if success)
        }
    except Exception as e:
        logger.error(f"❌ Bulk model download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_name}/status")
async def get_model_status(model_name: str, current_user = Depends(get_current_user)):
    """Get status of a specific model"""
    try:
        available = model_downloader.is_model_available(model_name)
        model_info = model_downloader.get_model_info(model_name) if available else None
        loaded = model_name in inference_engine.get_loaded_models()
        
        return {
            "status": "success",
            "model_name": model_name,
            "available": available,
            "loaded": loaded,
            "model_info": model_info
        }
    except Exception as e:
        logger.error(f"❌ Model status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_name}/load")
async def load_model(model_name: str, current_user = Depends(get_current_user)):
    """Load AI model into memory"""
    try:
        success = await inference_engine.load_model(model_name)
        if success:
            return {"status": "success", "message": f"Model {model_name} loaded successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to load model {model_name}")
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/models/{model_name}/unload")
async def unload_model(model_name: str, current_user = Depends(get_current_user)):
    """Unload AI model from memory"""
    try:
        inference_engine.unload_model(model_name)
        return {"status": "success", "message": f"Model {model_name} unloaded successfully"}
    except Exception as e:
        logger.error(f"❌ Model unloading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/malware")
async def analyze_file_for_malware(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    """Analyze uploaded file for malware"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Perform malware analysis
        result = await analyze_malware(file_content)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_size": len(file_content),
            "analysis_result": {
                "prediction": result.prediction,
                "confidence": result.confidence,
                "model_name": result.model_name,
                "inference_time": result.inference_time,
                "metadata": result.metadata
            }
        }
    except Exception as e:
        logger.error(f"❌ Malware analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/network-intrusion")
async def analyze_network_traffic(network_data: Dict[str, Any], current_user = Depends(get_current_user)):
    """Analyze network traffic for intrusions"""
    try:
        result = await detect_network_intrusion(network_data)
        
        return {
            "status": "success",
            "analysis_result": {
                "prediction": result.prediction,
                "confidence": result.confidence,
                "model_name": result.model_name,
                "inference_time": result.inference_time,
                "metadata": result.metadata
            }
        }
    except Exception as e:
        logger.error(f"❌ Network intrusion analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/logs")
async def analyze_system_logs(log_entries: List[str], current_user = Depends(get_current_user)):
    """Analyze system logs for anomalies"""
    try:
        result = await analyze_logs(log_entries)
        
        return {
            "status": "success",
            "log_count": len(log_entries),
            "analysis_result": {
                "prediction": result.prediction,
                "confidence": result.confidence,
                "model_name": result.model_name,
                "inference_time": result.inference_time,
                "metadata": result.metadata
            }
        }
    except Exception as e:
        logger.error(f"❌ Log analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/{model_name}")
async def make_prediction(model_name: str, data: Any, current_user = Depends(get_current_user)):
    """Make prediction using specific model"""
    try:
        result = await inference_engine.predict(model_name, data)
        
        return {
            "status": "success",
            "model_name": model_name,
            "prediction": result.prediction,
            "confidence": result.confidence,
            "inference_time": result.inference_time,
            "metadata": result.metadata
        }
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/loaded-models")
async def get_loaded_models(current_user = Depends(get_current_user)):
    """Get list of currently loaded models"""
    try:
        loaded_models = inference_engine.get_loaded_models()
        return {
            "status": "success",
            "loaded_models": loaded_models,
            "count": len(loaded_models)
        }
    except Exception as e:
        logger.error(f"❌ Failed to get loaded models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/malware-detector")
async def train_malware_detector(training_data: Dict[str, Any], current_user = Depends(get_current_user)):
    """Train a custom malware detection model"""
    try:
        # This would require processing the training data properly
        # For now, return a placeholder response
        return {
            "status": "success",
            "message": "Malware detector training initiated",
            "training_id": "train_001",
            "estimated_time": "30 minutes"
        }
    except Exception as e:
        logger.error(f"❌ Malware detector training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/anomaly-detector")
async def train_anomaly_detector(training_data: Dict[str, Any], current_user = Depends(get_current_user)):
    """Train a custom anomaly detection model"""
    try:
        # This would require processing the training data properly
        # For now, return a placeholder response
        return {
            "status": "success",
            "message": "Anomaly detector training initiated",
            "training_id": "train_002",
            "estimated_time": "20 minutes"
        }
    except Exception as e:
        logger.error(f"❌ Anomaly detector training failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/{training_id}/status")
async def get_training_status(training_id: str, current_user = Depends(get_current_user)):
    """Get status of model training job"""
    try:
        # Placeholder for training status check
        return {
            "status": "success",
            "training_id": training_id,
            "training_status": "in_progress",
            "progress": 65,
            "estimated_completion": "10 minutes"
        }
    except Exception as e:
        logger.error(f"❌ Training status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))