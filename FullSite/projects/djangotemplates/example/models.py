from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.TextField(max_length=500)

#class User_Stats(models.Model):
    #pass 
    #here will be user stats 