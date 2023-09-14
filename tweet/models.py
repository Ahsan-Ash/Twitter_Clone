from django.db import models
from user.models import User
# Create your models here.

class Tweet(models.Model):
    title = models.CharField(max_length = 25)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet')
