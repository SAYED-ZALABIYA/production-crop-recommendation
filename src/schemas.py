from pydantic import BaseModel, Field

class CropInput(BaseModel):
   
    nitrogen: float = Field(..., alias="Nitrogen (kg/ha )", description="Nitrogen content in soil")
    phosphorus: float = Field(..., alias="Phosphorus (kg/ha)", description="Phosphorus content in soil")
    potassium: float = Field(..., alias="Potassium (kg/ha)", description="Potassium content in soil")
    temperature: float = Field(..., alias="Temperature", description="Temperature in Celsius")
    humidity: float = Field(..., alias="Humidity", ge=0, le=100, description="Relative humidity in %")
    ph: float = Field(..., alias="pH_Value", ge=0, le=14, description="pH value of the soil")
    rainfall: float = Field(..., alias="Rainfall", ge=0, description="Rainfall in mm")

    class Config:
        populate_by_name = True