from django.db import models
from django.conf import settings

class Ad(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class ExchangeStatus(models.Model):
    name = models.CharField(max_length=40)

class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    ad_receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    status = models.ForeignKey(ExchangeStatus.name, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


