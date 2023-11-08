from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib import messages
# from django.contrib.contenttypes.models import ContentType
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse

import random
import os
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template.loader import render_to_string

# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

from datetime import datetime

from django.utils import timezone
import lyricsgenius
from dotenv import load_dotenv

from .models import Album, PlayList, Song, PlayListLike, AlbumLike, SongLike, User
from .forms import LoginForm, SignUpForm, PlayListForm, AlbumForm, EditUserForm

from .helpers import get_user_data, download_item, get_songs, add_song, create_item, like_item, send_otp_email, clean_song_title

OTP_EXPIRATION_TIME = 300  # 5 minutes


def home(request):
    """
    View for the home page.

    Renders the home page template with a greeting, playlists, and albums.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    current_time = timezone.localtime(timezone.now()).time()
    if current_time.hour >= 5 and current_time.hour < 12:
        greeting = 'Good morning'
    elif current_time.hour >= 12 and current_time.hour < 17:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'
        
    playlists = PlayList.objects.all().order_by('-created_at')[:20]
    user_playlist = PlayList.objects.filter(owner=request.user)[:5] if request.user.is_authenticated else []
    albums = Album.objects.all().order_by('-created_at')[:20]
    query = request.GET.get('query', '')
    if query:
        matching_songs = Song.objects.filter(song_name__icontains=query)
        playlist_ids = [song.content_object.id for song in matching_songs if song.content_object and song.content_type.model_class() == PlayList]
        album_ids = [song.content_object.id for song in matching_songs if song.content_object and song.content_type.model_class() == Album]
        
        playlists = PlayList.objects.filter(
            Q(playlist_name__icontains=query)|
            Q(owner__username__icontains=query)|
            Q(genre__name__icontains=query)|
            Q(description__icontains=query)|
            Q(id__in=playlist_ids)
        ).distinct()

        albums = Album.objects.filter(
            Q(album_name__icontains=query)|
            Q(owner__username__icontains=query)|
            Q(genre__name__icontains=query)|
            Q(description__icontains=query)|
            Q(id__in=album_ids)
        ).distinct()

    page_number = request.GET.get('page', 1)
    objects_per_page = 10

    p = Paginator(playlists, objects_per_page)
    
    try:
        playlist_page = p.page(page_number)
    except EmptyPage:
        playlist_page = p.page(1)
    
        
    context = {'playlists':playlist_page, 'user_playlist': user_playlist, 'albums':albums, 'greeting':greeting}

    return render(request, 'core/index.html', context)

def profile(request, username):
    """
    View for the user profile page.

    Retrieves user data and renders the profile template.

    Args:
        request: HttpRequest object.
        username (str): Username of the user.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    return get_user_data(request, username, 'core/profile.html')

def library(request, username):
    """
    View for the user library page.

    Retrieves user data and renders the library template.

    Args:
        request: HttpRequest object.
        username (str): Username of the user.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    return get_user_data(request, username, 'core/library.html')

@login_required
def liked(request):
    """
    View for the liked items page.

    Retrieves the user's liked items and renders the liked items template.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    user = get_object_or_404(User, id=request.user.id)

    return get_user_data(request, user.username, 'core/liked.html')

def liked_songs(request, pk):
    """
    View for displaying liked songs by a user.

    Retrieves the liked songs for a user and renders the liked songs template.

    Args:
        request: HttpRequest object.
        pk (int): Primary key of the user.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    name='songs'
    user = get_object_or_404(User, pk=pk)
    likedSongs = SongLike.objects.filter(user=user)
    
    context = {'liked_songs':likedSongs, 'name': name}
    
    return render(request, 'core/liked.html', context)

def isLiked(request):
    """
    View for checking if a song is liked by the current user.

    Checks if the song is liked by the current user and returns the result as a JSON response.

    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse: JSON response indicating if the song is liked.
    """

    pk = request.POST.get('id')
    user = request.user
    
    song = get_object_or_404(Song, pk=pk)
    likedSongs = list(SongLike.objects.filter(user=user))
    
    liked_Songs = [liked.song for liked in likedSongs if liked.song == song]
    
    return JsonResponse({'Liked': 'true'}) if liked_Songs else JsonResponse({'Liked': 'false'})


def editProfile(request, username):
    """
    View for editing a user's profile.

    Allows a user to edit their profile information and saves the changes.

    Args:
        request: HttpRequest object.
        username (str): Username of the user.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    user = User.objects.get(username=username)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'core/update-user.html', {'form': form})

@login_required
def likePlaylist(request):
    """
    View for liking a playlist.

    Handles the like functionality for a playlist.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response for liking a playlist.
    """

    return like_item(request, PlayList, PlayListLike, 'playlist_likes')

@login_required
def likeAlbum(request):
    """
    View for liking an album.

    Handles the like functionality for an album.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response for liking an album.
    """

    return like_item(request, Album, AlbumLike, 'album_likes')

@login_required
def likeSong(request, pk):
    """
    View for liking a song.

    Handles the like functionality for a song.

    Args:
        request: HttpRequest object.
        pk (int): Primary key of the song.

    Returns:
        JsonResponse: JSON response indicating the number of likes for the song.
    """

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        song = get_object_or_404(Song, pk=pk)
        liked = SongLike.objects.filter(user=request.user, song=song)

        if liked.exists():
            liked.delete()
        else:
            liked = SongLike.objects.create(user=request.user, song=song)
        songLikedCount = song.song_likes.count()
        return JsonResponse({'songLikedCount': songLikedCount})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def download_song(request, song_id):
    """
    View for downloading a song file.

    Allows the authenticated user to download a specific song file.

    Args:
        request: HttpRequest object.
        song_id (int): ID of the song.

    Returns:
        FileResponse: File response for downloading the song.
    """

    song = get_object_or_404(Song, id=song_id)
    file_path = song.music_file.path

    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def download_playlist(request, pk):
    """
    View for downloading a playlist.

    Allows the authenticated user to download a specific playlist.

    Args:
        request: HttpRequest object.
        pk (int): ID of the playlist.

    Returns:
        HttpResponse: Response for downloading the playlist.
    """

    return download_item(request, PlayList, pk)

@login_required
def download_album(request, pk):
    """
    View for downloading an album.

    Allows the authenticated user to download a specific album.

    Args:
        request: HttpRequest object.
        pk (int): ID of the album.

    Returns:
        HttpResponse: Response for downloading the album.
    """

    return download_item(request, Album, pk)


def playlistSongs(request, name, pk):
    """
    View for displaying the songs in a playlist.

    Retrieves the songs in a playlist and renders the playlist songs template.

    Args:
        request: HttpRequest object.
        name (str): Name of the playlist.
        pk (int): ID of the playlist.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    songs, playlist, is_liked, liked_songs = get_songs(request, PlayList, 'playlist_likes', pk)

    context = {
        'songs': songs,
        'playlist': playlist,
        'name': name,
        'playlist_id': pk,
        'is_liked': is_liked,
        'liked_songs': liked_songs
    }

    return render(request, 'core/playlist-songs.html', context)

def albumSongs(request, name, pk):
    """
    View for displaying the songs in an album.

    Retrieves the songs in an album and renders the album songs template.

    Args:
        request: HttpRequest object.
        name (str): Name of the album.
        pk (int): ID of the album.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    songs, album, is_liked, liked_songs = get_songs(request, Album, 'album_likes', pk)

    context = {
        'songs': songs,
        'album': album,
        'name': name,
        'playlist_id': pk,
        'is_liked': is_liked,
        'liked_songs': liked_songs
    }

    return render(request, 'core/album-songs.html', context)

def loginUser(request):
    """
    View for user login.

    Handles user authentication and login.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

def signUp(request):
    """
    View for user signup.

    Handles user registration, verification, and account creation.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response with the rendered template.
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if 'otp' in request.POST:
            current_time = datetime.now()
            if 'otp' in request.session and 'otp_time' in request.session:
                stored_otp_time = request.session['otp_time']
                if (current_time - stored_otp_time).total_seconds() <= OTP_EXPIRATION_TIME:
                    if request.POST['otp'] == request.session['otp']:
                        del request.session['otp']
                        del request.session['otp_time']
                        user = form.save()
                        login(request, user)
                        return redirect('core:home')
                    else:
                        message = 'Invalid OTP. Please try again.'
                        return render(request, 'core/signup.html', {'form': form, 'message': message})
                else:
                    del request.session['otp']
                    del request.session['otp_time']
                    message = 'OTP has expired. Please request a new OTP.'
                    return render(request, 'core/signup.html', {'form': form, 'message': message})
            else:
                message = 'OTP session not found. Please request a new OTP.'
                return render(request, 'core/signup.html', {'form': form, 'message': message})
        else:
            if form.is_valid():
                otp = str(random.randint(100000, 999999))
                send_otp_email(form.cleaned_data['email'], otp)
                request.session['otp'] = otp
                request.session['otp_time'] = datetime.now()
                return render(request, 'core/verify_otp.html', {'form': form, 'otp_sent': True})
            else:
                message = 'Looks like a username with that email or password already exists'
                return render(request, 'core/signup.html', {'form': form, 'message': message})
    else:
        form = SignUpForm()

    context = {'form': form}

    return render(request, 'core/signup.html', context)

def logoutUser(request):
    """
    View for user logout.

    Logs out the current user.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirects to the home page.
    """

    logout(request)

    return redirect('/')

@login_required
def createPlaylist(request):
    """
    View for creating a new playlist.

    Allows an authenticated user to create a new playlist.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response for creating a new playlist.
    """

    name = 'Playlist'

    return create_item(request, PlayListForm, PlayList, 'core:playlist-songs', 'playlist_name', name)

@login_required
def newAlbum(request):
    """
    View for creating a new album.

    Allows an authenticated user to create a new album.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Response for creating a new album.
    """

    if not request.user.verified:
        messages.error(request, 'You need to be a verified user to create an album.')
    
        return redirect('core:home')

    return create_item(request, AlbumForm, Album, 'core:album-songs', 'album_name')

@login_required
def addPlaylistSong(request, pk):
    """
    View for adding a song to a playlist.

    Allows an authenticated user to add a song to a specific playlist.

    Args:
        request: HttpRequest object.
        pk (int): ID of the playlist.

    Returns:
        HttpResponse: Response for adding a song to the playlist.
    """

    return add_song(request, PlayList, pk, 'playlist', 'playlist', 'playlist-songs')

@login_required
def addAlbumSong(request, pk):
    """
    View for adding a song to an album.

    Allows an authenticated user to add a song to a specific album.

    Args:
        request: HttpRequest object.
        pk (int): ID of the album.

    Returns:
        HttpResponse: Response for adding a song to the album.
    """

    return add_song(request, Album, pk, 'album', 'album', 'album-songs')

@login_required
def deleteSong(request, pk):
    """
    View for deleting a song.

    Allows an authenticated user to delete a specific song.

    Args:
        request: HttpRequest object.
        pk (int): ID of the song.

    Returns:
        JsonResponse: JSON response indicating the deletion of the song.
    """

    song = get_object_or_404(Song, pk=pk)
    song.delete()

    return JsonResponse({'message': 'Song Deleted' })

@login_required
def deletePlaylist(request, pk):
    """
    View for deleting a playlist.

    Allows an authenticated user to delete a specific playlist.

    Args:
        request: HttpRequest object.
        pk (int): ID of the playlist.

    Returns:
        HttpResponse: Response for deleting the playlist.
    """

    playlist = PlayList.objects.get(pk=pk)
    if request.method == "POST":
        playlist.delete()
        return redirect('/')
        # referer = request.META.get('HTTP_REFERER')
        # if referer:
        #     return redirect(referer)
        # else:
        #     return HttpResponse("Previous page not found.")

    return render(request, 'core/delete-confirmation.html', {'playlist': playlist})

@login_required
def editPlaylist(request, pk):
    """
    View for editing a playlist.

    Allows an authenticated user to edit a specific playlist.

    Args:
        request: HttpRequest object.
        pk (int): ID of the playlist.

    Returns:
        HttpResponse: Response with the rendered template for editing the playlist.
    """

    name = 'Playlist'
    playlist = get_object_or_404(PlayList, pk=pk)
    if request.method == 'POST':
        form = PlayListForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('core:playlist-songs', pk=pk)

    form = PlayListForm(instance=playlist)

    context = {'form': form, 'Playlist':name}

    return render(request, 'core/new.html', context)


def get_lyrics(request):
    """
    View for fetching song lyrics.

    Retrieves the lyrics of a song from the Genius API based on the provided artist and song title.

    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse: JSON response with the fetched song lyrics or an error message if the lyrics are not found.
    """

    load_dotenv()
    genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
    artist = request.POST.get('artist')
    print('Artist:',  artist)

    raw_title = request.POST.get('title')
    # print('Raw Title', raw_title)

    title = clean_song_title(raw_title)
    print('Cleaned title:', title)
    
    genius = lyricsgenius.Genius(genius_access_token, timeout=60)
    song = genius.search_song(title, artist)

    if song:
        # print(song.lyrics)
        return JsonResponse({
            'Artist': artist,
            'Title': title,
            'Lyrics': song.lyrics
        })
    else:
        # print("Not found")
        return JsonResponse({
            'error': 'Lyrics not found'
        })
