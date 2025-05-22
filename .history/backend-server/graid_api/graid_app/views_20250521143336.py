from django.shortcuts import render
from django.http import HttpResponse # For test URL
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.exceptions import ValidationError
import json
import random
from .models import Crop, Soil
from .recommendation_ai.src.services.recommendation_service import RecommendationService
from .recommendation_ai.src.models.recommendation_model import RecommendationModel
import pandas as pd
import requests

import threading
import time
from django.http import JsonResponse
import paho.mqtt.client as mqtt

# Global list to store messages temporarily
mqtt_messages = []

# MQTT Config
MQTT_BROKER = "a6faa28a33914e9bba541e6ec9da0741.s1.eu.hivemq.cloud"  # e.g., "abc123.s2.eu.hivemq.cloud"
MQTT_PORT = 8883  # For SSL (HiveMQ Cloud)
MQTT_USERNAME = "boztepe"
MQTT_PASSWORD = "Deneme123"
MQTT_TOPIC_SUBSCRIBE = "#"  # Subscribe to all topics (wildcard), or change to a specific one
MQTT_TOPIC_PUBLISH = "graid/measurement"
  # Topic to publish to


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Broker")
        client.subscribe(MQTT_TOPIC_SUBSCRIBE)
        # client.publish(MQTT_TOPIC_PUBLISH,'Subscribed')
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    if (msg.topic == 'graid/getMeasurements'):
        # Decode the message payload and convert to JSON
        try:
            payload = json.loads(msg.payload.decode())
             # Check if the payload contains a "measurements" key
            if "measurements" in payload and isinstance(payload["measurements"], list):
                measurements = payload["measurements"]

                # Add each measurement to the database
                # for measurement in measurements:
                #     add_soil_data(measurement)

                # Calculate the mean values for all measurements
                mean_measurement = calculate_mean_measurement(measurements)

                # Print the mean measurement for debugging
                print(f"Mean Measurement: {mean_measurement}")

                # Get AI recommendations for the mean measurement
                recommendations = getAIRecommendation(getValues(mean_measurement))
                print("Recommended Crop: ", recommendations)

                # Publish the recommendation back to the MQTT broker
                client.publish(MQTT_TOPIC_PUBLISH, json.dumps( recommendations))
            else:
                print("❌ Payload does not contain a valid 'measurements' array")
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON from message payload")
            return
        except Exception as e:
            print(f"❌ An error occurred: {e}")
    

# MQTT Start Function
mqtt_started = False
def start_mqtt():
    global mqtt_started
    if mqtt_started:
        return
    mqtt_started = True

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    # For HiveMQ Cloud, use SSL/TLS
    client.tls_set()  # Use default certificates

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_start()

    # thread = threading.Thread(target=client.loop_forever)
    # thread.daemon = True
    # thread.start()

def calculate_mean_measurement(measurements):
    # Initialize a dictionary to store the sum of each field
    mean_measurement = {
        "ph": 0,
        "temperature": 0,
        "humidity": 0,
        "nitrogen": 0,
        "phosphorus": 0,
        "potassium": 0,
        "ec": 0
    }

    # Iterate through each measurement and sum up the values
    for measurement in measurements:
        mean_measurement["ph"] += measurement.get("ph", 0)
        mean_measurement["temperature"] += measurement.get("temperature", 0)
        mean_measurement["humidity"] += measurement.get("humidity", 0)
        mean_measurement["nitrogen"] += measurement.get("nitrogen", 0)
        mean_measurement["phosphorus"] += measurement.get("phosphorus", 0)
        mean_measurement["potassium"] += measurement.get("potassium", 0)
        mean_measurement["ec"] += measurement.get("ec", 0)

    # Calculate the mean for each field
    num_measurements = len(measurements)
    for key in mean_measurement:
        mean_measurement[key] /= num_measurements

    return mean_measurement




recommendation_service = None


@api_view(['POST'])
def receive_data(request):
    try:
        if request.method == 'POST':
            received_data = request.data
            print("Received Data: ", received_data)
            
            
            # TODO Data processing will be done here (Can be done in other method)
            #add_soil_data(received_data)
            
            #recommendations = getAIRecommendation(getValues(received_data))
             # This funcition is here just for now to trying if it is adding to database
            return Response({"message": "OK", "received_data": received_data}, status=status.HTTP_200_OK)
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
    global recommendation_service

    soil_data = pd.read_csv('graid_app/recommendation_ai/src/data/soil_data.csv')
    
    recommendation_model = RecommendationModel(soil_data)
    recommendation_service = RecommendationService(recommendation_model)
    recommendation_service.train()
    print("Training model...")
    


def getValues(soil_data):

    ph=soil_data.get('ph'),
    temperature=soil_data.get('temperature'),
    humidity=soil_data.get('humidity'),
    nitrogen=soil_data.get('nitrogen'),
    phosphorus=soil_data.get('phosphorus'),
    potassium=soil_data.get('potassium'),
    ec=soil_data.get('ec'),
    print([float(nitrogen[0]), float(phosphorus[0]), float(potassium[0]), float(temperature[0]), float(humidity[0]), float(ph[0])])
    return [float(nitrogen[0]*100), float(phosphorus[0]*100), float(potassium[0]*100), float(temperature[0]), float(humidity[0]), float(ph[0])]


def getAIRecommendation(user_input):
    global recommendation_service
    recommended_crop = recommendation_service.predict(user_input)
    return recommended_crop


def test(request):
    return HttpResponse("Hello, world. You're at the Test View.")