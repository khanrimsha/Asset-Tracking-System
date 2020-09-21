
from django.db import models

# Create your models here.
class Location(models.Model):
    name=models.CharField(max_length=20)
    lat=models.FloatField()
    long=models.FloatField()
    def _unicode_(self):
        return self.name