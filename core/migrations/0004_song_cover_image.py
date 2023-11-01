# Generated by Django 4.2.6 on 2023-10-31 13:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_song_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='cover_image',
            field=models.ImageField(default='Logo1.png', upload_to=core.models.get_upload_path),
        ),
    ]