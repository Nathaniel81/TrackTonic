from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

class CommonFields(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to=user_dir, blank=True, null=True, default='Default.png')
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PlayList(CommonFields):
    playlist_name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.playlist_name

class Album(CommonFields):
    album_name = models.CharField(max_length=40)

    def __str__(self):
        return self.album_name

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PlayListLike(Like):
    playlist = models.ForeignKey(PlayList, related_name='playlist_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Playlist likes'

class AlbumLike(Like):
    album = models.ForeignKey(Album, related_name='album_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Album likes'

class Song(models.Model):
    song_name = models.CharField(max_length=40)
    # playlist = models.ForeignKey(PlayList, related_name='songs', on_delete=models.CASCADE)
    # album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    music_file = models.FileField(upload_to=user_dir_song)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.song_name

class SongLike(Like):
    song = models.ForeignKey(Song, related_name='song_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Song likes'