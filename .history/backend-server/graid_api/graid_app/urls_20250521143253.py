from django.urls import path
from .views import receive_data, test

urlpatterns = [
    path('receive-data', receive_data, name='receive_data'),  #URL of data sent by graid-app
    
    path("", test, name="test"), # Test URL

]
