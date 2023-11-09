"""
Module Description: This module contains helper functions used across different views in the application.
These helper functions aid in various tasks such as creating items, handling likes, sending OTP emails, and cleaning song titles.

Helper Functions:
- create_item: Creates an item based on the provided parameters.
- like_item: Handles the liking functionality for a specific item.
- send_otp_email: Sends an OTP email to the provided email address.
- clean_song_title: Cleans the song title by removing unnecessary parts.

Additional Information:
The functions in this module play a crucial role in the backend logic of various views and assist in simplifying and streamlining complex operations within the application.
"""

import os
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

from django.conf import settings
from django.http import HttpResponse, JsonResponse
import zipfile

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from mutagen import File

from django.core.mail import send_mail
import logging
import re

from .models import Album, Playlist, Song, PlaylistLike, AlbumLike, User, SongLike
from .forms import NewSongForm

# logger = logging.getLogger(__name__)


def get_user_data(request, username, template_name, name=None):
    """
    Retrieves user-related data for rendering the user's profile or library.

    Args:
        request: HttpRequest object.
        username (str): Username of the user.
        template_name (str): Template name for rendering the data.
        name (str, optional): Additional name parameter. Defaults to None.

    Returns:
        HttpResponse: Response for rendering the user's profile or library.
    """

    user = User.objects.get(username=username)
    liked_songs = SongLike.objects.filter(user=user)
    playlists = Playlist.objects.filter(owner=user)[:10]
    liked_playlists =  PlaylistLike.objects.filter(user=request.user)[:10]
    liked_albums =  AlbumLike.objects.filter(user=request.user)[:10]

    albums = Album.objects.filter(owner=user)[:10]
    context = {
        'user': user, 
        'playlists': playlists, 
        'albums': albums, 
        'liked_playlists': liked_playlists, 
        'liked_album':liked_albums,
        'liked_songs': liked_songs,
        'name': name
        }

    return render(request, template_name, context)

def download_item(request, model_class, pk):
    """
    Downloads an item and its associated content as a ZIP file.

    Args:
        request: HttpRequest object.
        model_class (class): Class of the model.
        pk (int): ID of the item.

    Returns:
        HttpResponse: Response for downloading the item as a ZIP file.
    """

    item = get_object_or_404(model_class, pk=pk)
    songs = Song.objects.filter(content_type=ContentType.objects.get_for_model(item), object_id=pk)

    if isinstance(item, Playlist):
        item_name = item.playlist_name
    elif isinstance(item, Album):
        item_name = item.album_name
    else:
        item_name = "item"

    zip_filename = f"{item_name}.zip"
    zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        # Adding songs to the zip
        for song in songs:
            song_file_path = os.path.join(settings.MEDIA_ROOT, str(song.music_file))
            zip_file.write(song_file_path, os.path.basename(song_file_path))

        # Adding item description as a text file
        if hasattr(item, 'description') and item.description:
            description_filename = f"{item_name}_description.txt"
            description_file_path = os.path.join(settings.MEDIA_ROOT, description_filename)
            with open(description_file_path, 'w') as description_file:
                description_file.write(item.description)
            zip_file.write(description_file_path, os.path.basename(description_file_path))
        else:
            default_description = f"No description available for this {model_class.__name__.lower()}."
            default_description_filename = f"{item_name}_description.txt"
            zip_file.writestr(default_description_filename, default_description)

    with open(zip_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        return response
    
def get_songs(request, model_class, liked_attr, pk):
    """
    Retrieves songs and related data based on the provided model and parameters.

    Args:
        request: HttpRequest object.
        model_class (class): Class of the model.
        liked_attr (str): Attribute for checking if the item is liked.
        pk (int): ID of the item.

    Returns:
        tuple: A tuple containing songs, the item, a boolean indicating if the item is liked, and liked songs.
    """

    item = get_object_or_404(model_class, pk=pk)
    songs = list(Song.objects.filter(content_type=ContentType.objects.get_for_model(item), object_id=pk))

    is_liked = False
    if request.user.is_authenticated:
        is_liked = getattr(item, liked_attr).filter(user=request.user).exists()

    if request.user.is_authenticated:
        liked_songs = [song for song in songs if song.song_likes.filter(user=request.user).exists()]
    else:
        liked_songs = []

    return songs, item, is_liked, liked_songs

def get_song_attributes(song, item):
    """
    Retrieves attributes for a song based on the provided song and item.

    Args:
        song: Song object.
        item: Item object.

    Returns:
        dict: A dictionary containing song attributes.
    """

    audio = EasyID3(song.temporary_file_path())
    artist_name = audio.get('artist', ['Unknown artist'])[0]
    # song_name = song.name
    duration = MP3(song.temporary_file_path()).info.length
    total_seconds = int(duration)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    duration_string = f"{minutes}:{seconds:02}"
    audio_tags = File(song.temporary_file_path())
    artist_name = audio_tags.get('TPE1', ['Unknown artist'])[0]
    song_name = audio_tags.get('TIT2', song.name)
    title = audio_tags.get('TIT2', 'Untitled')
    # print(audio_tags.keys())
    # print('song_name:' ,song_name)
    # print('title' ,title)
    
    cover_image = None

    # if 'APIC:' in audio_tags:
    for key in audio_tags.keys():
        if key.startswith('APIC:'):
            # print('APIC found')
            cover_data = audio_tags[key].data
            cover_image = ContentFile(cover_data, name='cover.jpg')
            break

    if not cover_image:
        default_image_path = os.path.join(settings.MEDIA_ROOT, "Logo1.png")
        with open(default_image_path, "rb") as f:
            cover_image = ContentFile(f.read(), name="Logo1.png")

    return {
        'song_name': song_name,
        'artist_name': artist_name,
        'duration': duration_string,
        'cover_image': cover_image,
        'item': item,
    }

def add_song(request, model_class, pk, item_name, item_field, redirect_name):
    """
    Adds a song to the provided model based on the specified parameters.

    Args:
        request: HttpRequest object.
        model_class (class): Class of the model.
        pk (int): ID of the item.
        item_name (str): Name of the item.
        item_field (str): Field of the item.
        redirect_name (str): Name for redirecting to the appropriate view.

    Returns:
        HttpResponse: Response for rendering the page to add songs.
    """

    item = model_class.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        music_files = request.FILES.getlist('music_file')
        if form.is_valid():
            for music in music_files:
                new_song = Song(content_object=item)
                new_song.music_file = music
                setattr(new_song, item_field, item)  # Functioning as a custom attribute to generate the upload path.
                new_song.content_type = ContentType.objects.get_for_model(model_class)
                new_song.object_id = item.id

                # try:
                song_attributes = get_song_attributes(music, item)
                print(f"Type of cover_image in add_song: {type(song_attributes['cover_image'])}")
                if song_attributes['cover_image'] is None:
                    raise ValueError("Cover image is None.")
                new_song.song_name = song_attributes['song_name']
                new_song.artist_name = song_attributes['artist_name']
                new_song.duration = song_attributes['duration']
                new_song.cover_image.save(f"{music.name}_cover.jpg", song_attributes['cover_image'], save=True)
                
                new_song.save()
                # except Exception as e:
                # logger.error(f"An error occurred: {e}")
            return redirect(f'core:{redirect_name}', name=getattr(item, f'{item_name}_name'), pk=pk)
    else:
        form = NewSongForm()
    context = {'form': form, item_name: item}

    return render(request, 'core/add-songs.html', context)

def create_item(request, form_class, item_class, redirect_name, item_name, name=None):
    """
    Creates an item based on the provided parameters.

    Args:
        request: HttpRequest object.
        form_class: Form class for the item.
        item_class: Class of the item.
        redirect_name: Name for redirecting to the appropriate view.
        item_name: Name of the item.
        name: Name for the item.

    Returns:
        HttpResponse: Response for rendering the new item page.
    """

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        name = form.data.get(item_name)
        existing_item = item_class.objects.filter(**{item_name: name, 'owner': request.user})

        if existing_item.exists():
            form.add_error(item_name, f'{item_class.__name__} name already exists!')
            context = {'form': form, 'item_name': name}
            return render(request, 'core/new.html', context)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect(redirect_name, **{'pk': item.pk, 'name': request.user.username})
    else:
        form = form_class()
    context = {'form': form, 'item_name': item_name, 'Playlist': name}

    return render(request, 'core/new.html', context)

def like_item(request, model_class, like_class, liked_attr):
    """
    Handles the liking functionality for a specific item.

    Args:
        request: HttpRequest object.
        model_class (class): Class of the model.
        like_class (class): Class of the like.
        liked_attr (str): Attribute for tracking the likes.

    Returns:
        JsonResponse: JSON response containing the like status and count.
    """

    is_liked = False
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_id = request.POST.get(f'{model_class.__name__.lower()}_id')
        item = get_object_or_404(model_class, pk=item_id)
        liked = like_class.objects.filter(user=request.user, **{model_class.__name__.lower(): item})
        if liked.exists():
            liked.delete()
        else:
            liked = like_class.objects.create(user=request.user, **{model_class.__name__.lower(): item})
            is_liked = True
        likes_count = getattr(item, liked_attr).count()

        return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def send_otp_email(email, otp):
    """
    Sends an OTP email to the provided email address.

    Args:
        email (str): Email address of the recipient.
        otp (str): One-time password for verification.
    """

    subject = 'OTP for Verification'
    message = f'Your OTP for verification is {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


def clean_song_title(title):
    """
    Cleans the song title by removing unnecessary parts.

    Args:
        title (str): Title of the song.

    Returns:
        str: Cleaned song title.
    """

    title = re.sub(r'\.mp3$', '', title)

    if 'feat.' in title.lower():
        title = re.sub(r'\s*\(feat\..*\)', '', title, flags=re.IGNORECASE)
    elif 'featuring' in title.lower():
        title = re.sub(r'\s*\(featuring.*\)', '', title, flags=re.IGNORECASE)

    match = re.search(r'\d+[-.]?\d*\s*(.+?)(\s*[-(].*)?$', title)
    if match:
        title = match.group(1)

    return title.strip()
