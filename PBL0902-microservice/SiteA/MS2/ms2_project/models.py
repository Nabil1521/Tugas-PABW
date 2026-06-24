from django.db import models

class TBCarsWeb(models.Model):
    carname = models.TextField()
    carbrand = models.TextField()
    carmodel = models.TextField()
    carprice = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'tbcarsweb'
