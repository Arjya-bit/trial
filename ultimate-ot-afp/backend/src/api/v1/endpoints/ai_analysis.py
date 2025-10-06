from fastapi import APIRouter

from src.modules.ai_model.model_inference import ModelService

router = APIRouter()
model_service = ModelService()


@router.get("/status")
def model_status():
    return model_service.status()


@router.post("/predict")
def predict(payload: dict):
    return {"prediction": model_service.predict(payload)}
