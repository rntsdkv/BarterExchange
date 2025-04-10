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

class StatusChoices(models.TextChoices):
    PENDING = "pending", "Ожидает"
    ACCEPTED = "accepted", "Принята"
    REJECTED = "rejected", "Отклонена"

class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_sent_proposals"
    )
    ad_receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_received_proposals"
    )
    comment = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)


