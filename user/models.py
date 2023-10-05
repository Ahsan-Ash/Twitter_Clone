from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length = 30)
    username = models.CharField(max_length= 12, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    name = models.CharField(max_length=30)
    phone_no = models.IntegerField(blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField()


