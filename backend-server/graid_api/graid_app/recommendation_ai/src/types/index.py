from typing import List, Dict, Any

class SoilData:
    def __init__(self, ph: float, nitrogen: float, phosphorus: float, potassium: float,temperature: float,ec: float, humidity: float):
        self.ph = ph
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.temperature = temperature
        self.ec = ec
        self.humidity = humidity


class CropRecommendation:
    def __init__(self, crop_name: str, suitability_score: float):
        self.crop_name = crop_name
        self.suitability_score = suitability_score

def get_soil_data_type() -> Dict[str, Any]:
    return {
        "ph": float,
        "nitrogen": float,
        "phosphorus": float,
        "potassium": float,
        "temperature": float,
        "ec": float,
        "humidity": float,

    }

def get_crop_recommendation_type() -> List[CropRecommendation]:
    return []