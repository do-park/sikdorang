from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    # profile_image = models.ImageField('프로필사진', blank=True, null=True)
    phone_number = models.CharField('휴대폰번호', blank=True, max_length=20)
    age = models.CharField('나이', blank=True, max_length=20)