"""
Module for defining signals in the Django application.

This module contains signal handlers for pre-deletion operations on the Song and PlayList models.
"""


import os
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Song, PlayList


@receiver(pre_delete, sender=Song)
def song_delete(sender, instance, **kwargs):
    """
    Signal handler to delete the associated file when a Song instance is deleted.

    Args:
        sender: The sender of the signal.
        instance: The instance of the Song model.
        **kwargs: Additional keyword arguments.
    """

    if instance.music_file:
        print("Song File Path:", instance.music_file.path)
        if os.path.isfile(instance.music_file.path):
            print("File Exists. Removing...")
            os.remove(instance.music_file.path)
        else:
            print("File does not exist")

@receiver(pre_delete, sender=PlayList)
def playlist_delete(sender, instance, **kwargs):
    """
    Signal handler to delete the associated file when a PlayList instance is deleted.

    Args:
        sender: The sender of the signal.
        instance: The instance of the PlayList model.
        **kwargs: Additional keyword arguments.
    """

    if instance.cover and instance.cover.path != os.path.join(settings.MEDIA_ROOT, 'Default.png'):
        print("Playlist Cover Path:", instance.cover.path)
        if os.path.isfile(instance.cover.path):
            print("File Exists. Removing...")
            os.remove(instance.cover.path)
        else:
            print("File does not exist")
    else:
        print("Default image. Skipping deletion...")
