# Generated by Django 3.1.7 on 2021-03-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210330_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='profile',
            name='headline',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
