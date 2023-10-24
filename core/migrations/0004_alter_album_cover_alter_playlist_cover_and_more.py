# Generated by Django 4.2.6 on 2023-10-24 06:44

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_albumlike_options_alter_playlistlike_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.user_dir),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.user_dir),
        ),
        migrations.AlterField(
            model_name='song',
            name='song_name',
            field=models.CharField(max_length=40),
        ),
    ]
