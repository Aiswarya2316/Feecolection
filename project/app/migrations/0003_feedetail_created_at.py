# Generated by Django 5.1.6 on 2025-02-11 08:37

from django.db import migrations, models
from django.utils.timezone import now


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_feedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
    ]
