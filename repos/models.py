from django.contrib.auth.models import User
from django.db import models


class Repo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=20)
