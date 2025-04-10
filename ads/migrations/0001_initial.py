# Generated by Django 5.2 on 2025-04-10 15:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ad",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="ads/images/")),
                ("category", models.CharField(max_length=100)),
                ("condition", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExchangeProposal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает"),
                            ("accepted", "Принята"),
                            ("rejected", "Отклонена"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "ad_receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="my_received_proposals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ad_sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="my_sent_proposals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
