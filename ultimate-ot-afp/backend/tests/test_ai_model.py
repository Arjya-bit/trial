def test_dummy_ai():
    from src.modules.ai_model.model_inference import predict_text
    result = predict_text("hello")
    assert "label" in result
