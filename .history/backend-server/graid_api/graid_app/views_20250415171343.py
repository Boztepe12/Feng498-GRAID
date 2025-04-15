from django.shortcuts import render
from django.http import HttpResponse # For test URL
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.exceptions import ValidationError
import json
from .models import Crop, Soil
from .recommendation_ai.src.services.recommendation_service import RecommendationService
from .recommendation_ai.src.models.recommendation_model import RecommendationModel
import pandas as pd
import requests





@api_view(['POST'])
def receive_data(request):
    try:
        if request.method == 'POST':
            received_data = request.data
            
            
            
            # TODO Data processing will be done here (Can be done in other method)
            #add_soil_data(received_data)
            
            recommendations = getAIRecommendation(getValues(received_data))
             # This funcition is here just for now to trying if it is adding to database
            return Response({"message": recommendations, "received_data": received_data}, status=status.HTTP_200_OK)
    except ValidationError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_confirmation():
    try:
        # Example URL and payload for the POST request
        url = "http://192.168.4.1:80/saveMeAsServer"
        payload = {
            "confirmationNum": "klj64!90jkolas"
        }

        # Sending the POST request
        response = requests.post(url, json=payload)

        # Handling the response
        if response.status_code == 200:
            response_data = response.json()

        else:
            response_data = {"error": f"Failed to fetch data, status code: {response.status_code}"}

        return response_data
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def add_soil_data(soil_data):
    # Adding soil data to database
    crop_name = soil_data.get('crop_name')
    crop, created = Crop.objects.get_or_create(name=crop_name) #created is a boolean value 
    # I put created value if we will need it in the future
    soil = Soil(
        ph=soil_data.get('ph'),
        temperature=soil_data.get('temperature'),
        humidity=soil_data.get('humidity'),
        nitrogen=soil_data.get('nitrogen'),
        phosphorus=soil_data.get('phosphorus'),
        potassium=soil_data.get('potassium'),
        ec=soil_data.get('ec'),
        soilMoisture=soil_data.get('soilMoisture'),
        crop=crop
    )
    soil.save()



def train_model():
    soil_data = pd.read_csv('graid_app/recommendation_ai/src/data/soil_data.csv')
    
    recommendation_model = RecommendationModel(soil_data)
    recommendation_service = RecommendationService(recommendation_model)
    recommendation_service.train()
    print("Training model...")
    return recommendation_service


def getValues(soil_data):
    ph=soil_data.get('ph'),
    temperature=soil_data.get('temperature'),
    humidity=soil_data.get('humidity'),
    nitrogen=soil_data.get('nitrogen'),
    phosphorus=soil_data.get('phosphorus'),
    potassium=soil_data.get('potassium'),
    ec=soil_data.get('ec'),
    return [float(nitrogen[0]), float(phosphorus[0]), float(potassium[0]), float(temperature[0]), float(humidity[0]), float(ph[0])]


def getAIRecommendation(user_input):
    recommendation_service = train_model()
    recommended_crop = recommendation_service.predict(user_input)
    return recommended_crop


def test(request):
    return HttpResponse("Hello, world. You're at the Test View.")