from django.shortcuts import render
from django.http import HttpResponse # For test URL
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import json

@api_view(['POST'])
def receive_data(request):
    try:
        if request.method == 'POST':
            try:
                received_data = json.loads(request.body)
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON data")
            # TODO Data processing will be done here (Can be done in other method)
            return Response({"message": "Data has been received", "received_data": received_data}, status=status.HTTP_200_OK)
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
    

def test(request):
    return HttpResponse("Hello, world. You're at the Test View.")