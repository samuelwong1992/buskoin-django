# Generated by Django 3.1.7 on 2021-03-31 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210331_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='snapchat_url',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_url',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]