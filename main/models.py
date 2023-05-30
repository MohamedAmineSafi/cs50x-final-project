from django.db import models
from users.models import User


# Create your models here.
class Friend(models.Model):
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=128)
    hobbies = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)
