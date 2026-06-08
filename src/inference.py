import joblib
import numpy as np
import os
from src.schemas import CropInput

class CropPredictor:
    def __init__(self, models_dir: str = "models"):
        self.model = joblib.load(os.path.join(models_dir, "best_random_forest_model.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        self.encoder = joblib.load(os.path.join(models_dir, "label_encoder.pkl"))

    def predict(self, payload: CropInput) -> dict:
        features = np.array([
            payload.nitrogen, 
            payload.phosphorus, 
            payload.potassium,
            payload.temperature, 
            payload.humidity, 
            payload.ph, 
            payload.rainfall
        ]).reshape(1, -1)

        scaled_features = self.scaler.transform(features)
        
       
        probabilities = self.model.predict_proba(scaled_features)
        confidence_score = np.max(probabilities)
        
        predicted_class = self.model.predict(scaled_features)[0]
        
        recommended_crop = self.encoder.inverse_transform([predicted_class])[0]

        return {
            "recommended_crop": str(recommended_crop),
            "confidence_score": round(float(confidence_score) * 100, 2)
        }
