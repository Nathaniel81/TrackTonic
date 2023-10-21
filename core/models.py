import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_img(instance, filename):
    return f'user_{instance.id}/{filename}'

def user_dir(instance, filename):
    return f'user_{instance.owner.id}/{filename}'

def user_dir_song(instance, filename):
    return f'user_{instance.playlist.owner.id}/{filename}'

class User(AbstractUser):
    name = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(upload_to=user_img, null=True, blank=True, default='avatar.svg')
    bio = models.TextField(max_length=300, null=True, blank=True)
    verified = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name

class PlayList(models.Model):
    playlist_name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    genre = models.CharField(max_length=200)
    cover = models.ImageField(upload_to=user_dir, blank=True, null=True, help_text=".jpg, .png, .jpeg, .gif, .svg supported")
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.playlist_name

class PlayListLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(PlayList, related_name='playlist-likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Album(models.Model):
    album_name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    genre = models.CharField(max_length=200)
    cover = models.ImageField(upload_to=user_dir, blank=True, null=True, help_text=".jpg, .png, .jpeg, .gif, .svg supported")
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.album_name
class AlbumLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='album-likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Song(models.Model):
    song_name = models.CharField(max_length=40, help_text=".mp3 supported only",)
    playlist = models.ForeignKey(PlayList, related_name='songs', on_delete=models.CASCADE)
    music_file = models.FileField(upload_to=user_dir_song)

    def __str__(self):
        return self.song_name

class SongLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='song-likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

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
