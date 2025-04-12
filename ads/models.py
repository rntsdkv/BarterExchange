import os

from django.db import models
from django.conf import settings

class AdCondition(models.TextChoices):
    NEW = "new", "Новый"
    USED = "used", "Б/у"

class AdStatus(models.TextChoices):
    ACTIVE = "active", "Активное"
    EXCHANGED = "exchanged", "Обменяли"

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
    status = models.CharField(
        max_length=10,
        choices=AdStatus.choices,
        default=AdStatus.ACTIVE
    )

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

class StatusChoices(models.TextChoices):
    PENDING = "pending", "Ожидает"
    ACCEPTED = "accepted", "Принята"
    REJECTED = "rejected", "Отклонена"

class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.status = StatusChoices.ACCEPTED
        self.ad_sender.status = AdStatus.EXCHANGED
        self.ad_receiver.status = AdStatus.EXCHANGED
        self.ad_sender.save()
        self.ad_receiver.save()
        self.save()

    def reject(self):
        self.status = StatusChoices.REJECTED
        self.save()
