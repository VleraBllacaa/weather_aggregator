# Generated by Django 5.1.3 on 2024-11-08 11:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bulgarian_meteo_pro", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bulgarianmeteoprodata",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
