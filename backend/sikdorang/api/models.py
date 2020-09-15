from django.db import models

class Tags(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    def __str__ (self):
        return self.name

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    def __str__ (self):
        return self.name

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, null=True)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    tags = models.ManyToManyField(Tags, related_name = 'store_tags') 
    category = models.ManyToManyField(Category, related_name = 'store_category')