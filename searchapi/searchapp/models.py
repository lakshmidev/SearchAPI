from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True)

class ApiReport(models.Model):
    """Stores seach API call details"""
    search_keyword = models.CharField(max_length=255, blank=True)
    api_call_date = models.DateField(null=True, blank=True)