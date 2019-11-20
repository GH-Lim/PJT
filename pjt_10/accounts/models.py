from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# User 모델 Customizing
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings'
    )
