from random import randint

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    user_code = models.IntegerField(default=0)
    profile_image = models.ImageField('프로필사진', default='/profile/default.jpg', upload_to="profile/")
    phone_number = models.CharField('휴대폰번호', blank=True, max_length=20)
    age = models.CharField('나이', blank=True, max_length=20)
    done_cup = models.BooleanField(default=False)
    

class UserPhoneCheck(models.Model):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'user_phone_check'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)