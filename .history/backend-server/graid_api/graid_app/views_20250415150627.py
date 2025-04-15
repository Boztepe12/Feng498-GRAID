from django.shortcuts import render
from django.http import HttpResponse # For test URL
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import json
from .models import Crop, Soil
from .recommendation_ai.src.services.recommendation_service import RecommendationService
from .recommendation_ai.src.models.recommendation_model import RecommendationModel

@api_view(['POST'])
def receive_data(request):
    try:
        if request.method == 'POST':
            received_data = request.data
            
            
            
            # TODO Data processing will be done here (Can be done in other method)
            #add_soil_data(received_data)
            
            recommendations = getAIRecommendation(getValues(received_data)).toString()
             # This funcition is here just for now to trying if it is adding to database
            return Response({"message": recommendations, "received_data": received_data}, status=status.HTTP_200_OK)
    except ValidationError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def send_data(request):
    try:
        # Processed data to be sent
        processed_data = {
            "crop_name": "Velvet Cotton",
            "percentage_of_choice": 80,
            "AI's comment": "This crop is best suited for your farm"
        }
        return Response({"message": "Processed data sent", "data": processed_data}, status=status.HTTP_200_OK)
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


def getValues(soil_data):
    ph=soil_data.get('ph'),
    temperature=soil_data.get('temperature'),
    humidity=soil_data.get('humidity'),
    nitrogen=soil_data.get('nitrogen'),
    phosphorus=soil_data.get('phosphorus'),
    potassium=soil_data.get('potassium'),
    ec=soil_data.get('ec'),
    return [nitrogen, phosphorus, potassium, temperature, humidity]


def getAIRecommendation(soil_data):
    # Assuming soil_data is a list of features

    recommendation_model = RecommendationModel(soil_data)
    recommendation_service = RecommendationService(recommendation_model)
    recommendation_service.train()

    recommended_crop = recommendation_service.predict(soil_data)
    return recommended_crop

def test(request):
    return HttpResponse("Hello, world. You're at the Test View.")