# Generated by Django 5.1.4 on 2025-01-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='download_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
