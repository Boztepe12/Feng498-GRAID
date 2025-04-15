# filepath: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\backend-server\graid_api\graid_app\apps.py
from django.apps import AppConfig
from .recommendation_ai.src.services.recommendation_service import RecommendationService
import threading

class GraidAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graid_app'

    def ready(self):
        
        from .views import train_model,send_confirmation

        
        threading.Thread(target=send_confirmation).start()
        threading.Thread(target=train_model).start()
