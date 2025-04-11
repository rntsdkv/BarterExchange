import os

from django.db import models
from django.conf import settings

class AdCondition(models.TextChoices):
    NEW = "new", "Новый"
    USED = "used", "Б/у"

class AdCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Ad(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_ads',
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    condition = models.CharField(
        max_length=10,
        choices=AdCondition.choices,
        default=AdCondition.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

class StatusChoices(models.TextChoices):
    PENDING = "pending", "Ожидает"
    ACCEPTED = "accepted", "Принята"
    REJECTED = "rejected", "Отклонена"

class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_sender_id')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_receiver_id')
    comment = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)


