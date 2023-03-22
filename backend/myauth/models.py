from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    @staticmethod
    def get_by_user(user):
        return UserProfile.objects.get_or_create(user=user)[0] if user else None

    def __str__(self):
        return str(self.user)
