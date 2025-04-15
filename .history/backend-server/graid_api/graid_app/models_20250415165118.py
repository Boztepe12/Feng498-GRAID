from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class Soil(models.Model):
    ph = models.FloatField()
    ec = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    soilMoisture = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)

    def __str__(self):
        return f"Soil data for {self.crop.name}"

class Model(models.Model):
    name = models.CharField(max_length=100)
    model_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name