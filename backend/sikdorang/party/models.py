from django.db import models
from django.conf import settings
from trip.models import Trip

# Create your models here.

class Party(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PartyMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    content = models.TextField()