from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.

class AuthModel(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    home_address = models.TextField()
    
    username = models.CharField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    


class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    ISBN = models.CharField(max_length=20)
    pbulisher = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    image = CloudinaryField('LBRY/books', blank=True, null=True)
