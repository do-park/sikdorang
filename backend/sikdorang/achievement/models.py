from django.db import models
from django.conf import settings

class AchiveStore(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    image = models.ImageField()
    description = models.TextField()