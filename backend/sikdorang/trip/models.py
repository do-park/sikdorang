from django.db import models
from django.conf import settings

# Create your models here.

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    plan = models.TextField()
    date = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    party_chk = models.IntegerField(default=0)