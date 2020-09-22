from django.db import models
from django.conf import settings

# Create your models here.

class TripItemModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title_img = models.ImageField(blank=True, upload_to="guide/%Y/%m/%d")
    title = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    start_date = models.CharField(max_length=30)
    end_date = models.CharField(max_length=30)
    price = models.IntegerField()
    start_point = models.CharField(max_length=50)
    start_time = models.CharField(max_length=30)
    content = models.TextField()