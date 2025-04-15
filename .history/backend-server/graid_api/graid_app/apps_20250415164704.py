# filepath: c:\Users\Ege Deniz\Documents\GitHub\Feng498-GRAID\backend-server\graid_api\graid_app\apps.py
from django.apps import AppConfig
import threading

class GraidAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graid_app'

    def ready(self):
        # Import the function you want to fire
        from .views import some_function_to_fire

        # Run the function in a separate thread to avoid blocking the server
        threading.Thread(target=some_function_to_fire).start()
