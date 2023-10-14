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
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name

class PlayList(models.Model):
    playlist_name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    genre = models.CharField(max_length=200)
    cover = models.ImageField(upload_to=user_dir, blank=True, null=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.playlist_name

class Song(models.Model):
    song_name = models.CharField(max_length=40)
    playlist = models.ForeignKey(PlayList, related_name='songs', on_delete=models.CASCADE)
    music_file = models.FileField(upload_to=user_dir_song)

    def __str__(self):
        return self.song_name
