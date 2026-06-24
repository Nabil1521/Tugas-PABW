# models.py
from django.db import models

class Car(models.Model):
    carname = models.CharField(max_length=100)
    carbrand = models.CharField(max_length=100)
    carmodel = models.CharField(max_length=100)
    carprice = models.IntegerField()

    def __str__(self):
        return self.carname