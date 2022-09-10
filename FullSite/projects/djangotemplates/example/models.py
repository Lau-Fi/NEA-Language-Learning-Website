from django.db import models

class Question(models.Model):
    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)
