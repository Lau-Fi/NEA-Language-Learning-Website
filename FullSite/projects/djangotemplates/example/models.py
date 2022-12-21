from django.db import models
from django.contrib.auth.models import User


class Lang(models.Model):
    lang_name = models.TextField(max_length=500)


class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    difficulty = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.TextField(max_length=500)

class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    correct_answers = models.TextField(max_length=500)
    wrong_answers = models.TextField(max_length=500)
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)
    difficulty = models.IntegerField() 



