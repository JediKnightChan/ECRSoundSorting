from django.db import models


class TelegramNotification(models.Model):
    app_name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    model_id = models.IntegerField()
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
