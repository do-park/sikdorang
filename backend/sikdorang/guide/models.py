from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

# Create your models here.

class TripItemModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title_img = models.ImageField(blank=True, upload_to="guide/%Y/%m/%d")
    title = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    price = models.IntegerField()
    start_point = models.CharField(max_length=50)
    start_time = models.CharField(max_length=30)
    content = models.TextField()
    limit_person = models.IntegerField()
    departure_person = models.IntegerField()
    now_person = models.IntegerField(default=0)

class GuideTour(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip_item = models.ForeignKey(TripItemModel, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)