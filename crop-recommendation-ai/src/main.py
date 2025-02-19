# File: /crop-recommendation-ai/crop-recommendation-ai/src/main.py

import pandas as pd
from services.recommendation_service import RecommendationService
from utils.file_reader import read_csv

def main():
    # Load soil data
    soil_data = read_csv('data/soil_data.csv')
    
    # Initialize the recommendation service
    recommendation_service = RecommendationService(soil_data)
    
    # Example server input (this could be replaced with actual server input handling)
    user_input = {
        'ph': 6.5,
        'nitrogen': 50,
        'phosphorus': 30,
        'potassium': 40,
        'temperature': 25,
        'rainfall': 100
    }
    
    # Get crop recommendations
    recommendations = recommendation_service.get_recommendations(user_input)
    
    # Print recommendations
    print("Recommended crops based on the provided soil data:")
    for crop in recommendations:
        print(crop)

if __name__ == "__main__":
    main()