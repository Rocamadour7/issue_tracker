from django.contrib.auth.models import User
from django.db import models


class Repo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.SlugField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Issue(models.Model):
    ISSUE_STATE = (
        ('o', 'open'),
        ('s', 'stale'),
        ('p', 'in progress'),
        ('r', 'resolved'),
    )
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    title = models.SlugField(max_length=100)
    body = models.TextField()
    author = models.CharField(max_length=100)
    state = models.CharField(max_length=1, choices=ISSUE_STATE, default='o')
    created_at = models.DateTimeField()
    due_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
