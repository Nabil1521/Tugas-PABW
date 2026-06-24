from django.db import models


class Car(models.Model):
    carname = models.TextField()
    carbrand = models.TextField()
    carmodel = models.TextField()
    carprice = models.TextField()

    class Meta:
        db_table = 'api_car'

    def __str__(self):
        return f"{self.carname} - {self.carbrand}"
