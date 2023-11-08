"""
Models for the Django application.

This module contains the models used for defining various entities 
such as users, playlists, albums, likes, and songs within the application.
"""


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def user_img(instance, filename):
    """
    Function to define the upload path for user avatars.

    Args:
        instance: Instance of the User model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the avatar.
    """

    return f'user_{instance.id}/{filename}'

def user_dir(instance, filename):
    """
    Function to define the upload path for files associated with the user.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.owner.id}/{filename}'

def user_dir_playlist_song(instance, filename):
    """
    Function to define the upload path for files associated with a playlist's song.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.playlist.owner.id}/{filename}'

def user_dir_album_song(instance, filename):
    """
    Function to define the upload path for files associated with an album's song.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file.
    """

    return f'user_{instance.album.owner.id}/{filename}'

def get_upload_path(instance, filename):
    """
    Function to get the upload path based on the instance and filename.

    Args:
        instance: Instance of the model.
        filename (str): Original filename.

    Returns:
        str: The upload path for the file based on the instance type.
    """

    if hasattr(instance, 'playlist'):
        return user_dir_playlist_song(instance, filename)
    else:
        return user_dir_album_song(instance, filename)


@deconstructible
class MusicFileValidator:
    """
    Validator class for music files.

    This class checks if the file has a valid extension.
    """

    def __call__(self, value):
        """
        Validate the music file.

        Args:
            value: The value to be validated.

        Raises:
            ValidationError: If the file extension is not supported.
        """

        valid_extensions = ['mp3', 'm4a','wav', 'ogg', 'flac']
        ext = value.name.split('.')[-1]
        print(f"File extension: {ext}")
        print(f"Valid extensions: {valid_extensions}")
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')


class User(AbstractUser):
    """
    Custom user model for the application.

    Attributes:
        name (str): The name of the user.
        email (str): The email of the user.
        avatar (ImageField): The avatar of the user.
        bio (str): The biography of the user.
        verified (bool): Indicates whether the user is verified or not.
        total_likes (int): The total number of likes received by the user.
    """

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
    """
    Model representing music genres.

    Attributes:
        name (str): The name of the genre.
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

class CommonFields(models.Model):
    """
    Abstract model class defining common fields shared by Playlist and Album models.

    Attributes:
        owner (ForeignKey): The owner of the playlist or album.
        genre (ForeignKey): The genre associated with the playlist or album.
        cover (ImageField): The cover image of the playlist or album.
        description (TextField): Description of the playlist or album.
        created_at (DateTimeField): Date and time when the playlist or album was created.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to=user_dir, blank=True, null=True, default='Default.png')
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PlayList(CommonFields):
    """
    Model representing a playlist in the application.

    Attributes:
        playlist_name (str): The name of the playlist.
    """

    playlist_name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.playlist_name

class Album(CommonFields):
    """
    Model representing an album in the application.

    Attributes:
        album_name (str): The name of the album.
    """

    album_name = models.CharField(max_length=40)

    def __str__(self):
        return self.album_name

class Like(models.Model):
    """
    Abstract model class defining a generic model for likes.

    Attributes:
        user (ForeignKey): The user who liked the content.
        timestamp (DateTimeField): The date and time when the like was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PlayListLike(Like):
    """
    Model representing a like on a playlist.

    Attributes:
        playlist (ForeignKey): The playlist that was liked.
    """

    playlist = models.ForeignKey(PlayList, related_name='playlist_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Playlist likes'

class AlbumLike(Like):
    """
    Model representing a like on an album.

    Attributes:
        album (ForeignKey): The album that was liked.
    """

    album = models.ForeignKey(Album, related_name='album_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Album likes'

class Song(models.Model):
    """
    Model representing a song in the application.

    Attributes:
        song_name (str): The name of the song.
        artist_name (str): The name of the artist.
        content_type (ForeignKey): The content type of the song.
        object_id (PositiveIntegerField): The ID of the object.
        content_object (GenericForeignKey): The content object.
        music_file (FileField): The music file of the song.
        duration (str): The duration of the song.
        cover_image (ImageField): The cover image of the song.
        genre (ForeignKey): The genre of the song.
    """

    song_name = models.CharField(max_length=40)
    artist_name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    music_file = models.FileField(upload_to=get_upload_path, validators=[MusicFileValidator()])
    duration = models.CharField(max_length=10)
    cover_image = models.ImageField(upload_to=get_upload_path, default="Logo1.png")
    # music_file = models.FileField(upload_to=get_upload_path)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.song_name

class SongLike(Like):
    """
    Model representing a like on a song.

    Attributes:
        song (ForeignKey): The song that was liked.
    """

    song = models.ForeignKey(Song, related_name='song_likes', on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Song likes'
