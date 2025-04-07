# File: /crop-recommendation-ai/crop-recommendation-ai/src/main.py

import pandas as pd
from services.recommendation_service import RecommendationService
from utils.file_reader import read_csv
from models.recommendation_model import RecommendationModel

def main():
    # Load soil data
    soil_data = read_csv('data/soil_data.csv')
    
    
    # Initialize the recommendation model
    recommendation_model = RecommendationModel(soil_data)
    
    # Initialize the recommendation service
    recommendation_service = RecommendationService(recommendation_model)
    recommendation_service.train()
    
    

if __name__ == "__main__":
    main()