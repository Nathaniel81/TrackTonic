import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Song, PlayList

@receiver(pre_delete, sender=Song)
def song_delete(sender, instance, **kwargs):
    if instance.music_file:
        print("Song File Path:", instance.music_file.path)
        if os.path.isfile(instance.music_file.path):
            print("File Exists. Removing...")
            os.remove(instance.music_file.path)
        else:
            print("File does not exist")

@receiver(pre_delete, sender=PlayList)
def playlist_delete(sender, instance, **kwargs):
    if instance.cover:
        print("Playlist Cover Path:", instance.cover.path)
        if os.path.isfile(instance.cover.path):
            print("File Exists. Removing...")
            os.remove(instance.cover.path)
        else:
            print("File does not exist")
