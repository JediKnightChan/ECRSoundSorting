from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_edited_timestamp = models.DateTimeField(auto_now=True)
