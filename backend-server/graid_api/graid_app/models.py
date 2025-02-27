from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
