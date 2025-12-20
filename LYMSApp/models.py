from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class AuthModel(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    home_address = models.TextField()
    
    username = models.CharField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
