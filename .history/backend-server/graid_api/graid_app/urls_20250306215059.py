from django.urls import path
from .views import receive_data, send_data, test

urlpatterns = [
    path('receive-data/', receive_data, name='receive_data'),  #URL of data sent by graid-app
    path('send-data/', send_data, name='send_data'),  # URL of data to be sent to graid-app
    path("", test, name="test"), # Test URL
]
