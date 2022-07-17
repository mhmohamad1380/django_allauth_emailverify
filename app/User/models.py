import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    verify_token = models.CharField(max_length=256,blank=False,null=True)
    verify_token_time = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    