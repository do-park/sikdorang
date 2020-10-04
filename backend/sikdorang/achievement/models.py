from django.db import models
from django.conf import settings

class Themes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    def __str__ (self):
        return self.name

class AchiveStore(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    image = models.ImageField()
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE)
    description = models.TextField()
    def __str__ (self):
        return self.store_name

class ThemeUser(models.Model):
    count = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class AchieveUser(models.Model):
    count = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receipt = models.ImageField('영수증사진', upload_to="receipt/%Y/%m/%d")
