from fastapi import APIRouter
from ....modules.ai_model.model_inference import predict_text

router = APIRouter()


@router.post("/analyze")
def analyze(payload: dict):
    text = payload.get("text", "")
    prediction = predict_text(text)
    return {"input": text, "prediction": prediction}
