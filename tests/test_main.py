import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock




with patch('src.inference.CropPredictor') as mock_predictor_class:
    mock_instance = MagicMock()
    mock_instance.predict.return_value = {
        "recommended_crop": "rice",
        "confidence_score": 0.95
    }
    mock_predictor_class.return_value = mock_instance

    from src.main import app

client = TestClient(app)

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_successful_prediction():
    with TestClient(app) as client:
        payload = {
            "Nitrogen (kg/ha )": 90.0,
            "Phosphorus (kg/ha)": 42.0,
            "Potassium (kg/ha)": 43.0,
            "Temperature": 20.8,
            "Humidity": 82.0,
            "pH_Value": 6.5,
            "Rainfall": 202.9
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "recommended_crop" in data
        assert "confidence_score" in data

def test_invalid_validation_ph():
    with TestClient(app) as client:
        payload = {
            "Nitrogen (kg/ha )": 90.0,
            "Phosphorus (kg/ha)": 42.0,
            "Potassium (kg/ha)": 43.0,
            "Temperature": 20.8,
            "Humidity": 82.0,
            "pH_Value": 16.0,
            "Rainfall": 202.9
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
