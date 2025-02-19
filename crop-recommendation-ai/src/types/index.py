from typing import List, Dict, Any

class SoilData:
    def __init__(self, ph: float, moisture: float, nitrogen: float, phosphorus: float, potassium: float):
        self.ph = ph
        self.moisture = moisture
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium

class CropRecommendation:
    def __init__(self, crop_name: str, suitability_score: float):
        self.crop_name = crop_name
        self.suitability_score = suitability_score

def get_soil_data_type() -> Dict[str, Any]:
    return {
        "ph": float,
        "moisture": float,
        "nitrogen": float,
        "phosphorus": float,
        "potassium": float
    }

def get_crop_recommendation_type() -> List[CropRecommendation]:
    return []