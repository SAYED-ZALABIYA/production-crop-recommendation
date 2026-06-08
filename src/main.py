import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.schemas import CropInput
from src.inference import CropPredictor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(">>> [STARTUP] Loading machine learning models into memory...")
    try:
        ml_models["predictor"] = CropPredictor()
        logger.info(">>> [STARTUP] Models loaded successfully! Server is ready.")
    except Exception as e:
        logger.error(f">>> [STARTUP ERROR] Failed to load models: {str(e)}")
        raise e
    yield
    logger.info(">>> [SHUTDOWN] Cleaning up resources and shutting down...")
    ml_models.clear()

app = FastAPI(
    title="Production Crop Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict_crop(payload: CropInput):
    try:
        logger.info("Received prediction request via /predict endpoint")
        predictor = ml_models.get("predictor")
        if not predictor:
            raise HTTPException(status_code=503, detail="Model service is not initialized yet.")
            
        result = predictor.predict(payload)
        logger.info(f"Prediction successful. Recommended: {result['recommended_crop']}")
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error during inference: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
