"""
AI Analysis API Endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from ....modules.ai_model.model_downloader import download_kaggle_model, CYBERSECURITY_MODELS
from ....modules.ai_model.model_inference import get_inference_engine

router = APIRouter()


class PredictionRequest(BaseModel):
    features: Dict[str, Any]


class NetworkAnalysisRequest(BaseModel):
    packet_data: Dict[str, Any]


class ModelDownloadRequest(BaseModel):
    model_key: str
    username: Optional[str] = None
    api_key: Optional[str] = None


@router.post("/predict")
async def make_prediction(request: PredictionRequest):
    """Make AI prediction on input data"""
    try:
        engine = get_inference_engine()
        result = engine.predict(request.features)
        return {"status": "success", "prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-network")
async def analyze_network_traffic(request: NetworkAnalysisRequest):
    """Analyze network traffic using AI"""
    try:
        engine = get_inference_engine()
        result = engine.analyze_network_traffic(request.packet_data)
        return {"status": "success", "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-malware")
async def analyze_malware(features: Dict[str, Any]):
    """Analyze malware using AI"""
    try:
        engine = get_inference_engine()
        result = engine.analyze_malware(features)
        return {"status": "success", "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/available")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "status": "success",
        "models": CYBERSECURITY_MODELS
    }


@router.post("/models/download")
async def download_model(request: ModelDownloadRequest, background_tasks: BackgroundTasks):
    """Download AI model from Kaggle"""
    try:
        async def download_task():
            await download_kaggle_model(
                CYBERSECURITY_MODELS[request.model_key]["dataset"],
                request.username,
                request.api_key
            )
        
        background_tasks.add_task(download_task)
        
        return {
            "status": "success",
            "message": "Model download started",
            "model": request.model_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/load")
async def load_model(model_file: str = "model.pkl"):
    """Load AI model for inference"""
    try:
        engine = get_inference_engine()
        engine.load_model(model_file)
        return {"status": "success", "message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
