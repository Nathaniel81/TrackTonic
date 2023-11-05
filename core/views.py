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
from django.core.mail import send_mail
from django.conf import settings
# from django.template.loader import render_to_string

# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

from datetime import datetime

from django.utils import timezone

from .models import Album, PlayList, Song, PlayListLike, AlbumLike, SongLike, User
from .forms import LoginForm, SignUpForm, PlayListForm, AlbumForm, EditUserForm

from .helpers import get_user_data, download_item, get_songs, add_song, create_item, like_item, send_otp_email

OTP_EXPIRATION_TIME = 300  # 5 minutes


def home(request):
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
    return get_user_data(request, username, 'core/profile.html')

def library(request, username):
    return get_user_data(request, username, 'core/library.html')

@login_required
def liked(request):
    user = get_object_or_404(User, id=request.user.id)
    return get_user_data(request, user.username, 'core/liked.html')

def liked_songs(request, pk):
    name='songs'
    user = get_object_or_404(User, pk=pk)
    likedSongs = SongLike.objects.filter(user=user)
    
    context = {'liked_songs':likedSongs, 'name': name}
    
    return render(request, 'core/liked.html', context)

def isLiked(request, pk):
    user = request.user
    
    song = get_object_or_404(Song, pk=pk)
    likedSongs = list(SongLike.objects.filter(user=user))
    
    liked_Songs = [liked.song for liked in likedSongs if liked.song == song]
    
    return JsonResponse({'Liked': 'true'}) if liked_Songs else JsonResponse({'Liked': 'false'})


def editProfile(request, username):
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
    return like_item(request, PlayList, PlayListLike, 'playlist_likes')

@login_required
def likeAlbum(request):
    return like_item(request, Album, AlbumLike, 'album_likes')

@login_required
def likeSong(request, pk):
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
    song = get_object_or_404(Song, id=song_id)
    file_path = song.music_file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def download_playlist(request, pk):
    return download_item(request, PlayList, pk)

@login_required
def download_album(request, pk):
    return download_item(request, Album, pk)


def playlistSongs(request, name, pk):
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
    logout(request)
    
    return redirect('/')

@login_required
def createPlaylist(request):
    name = 'Playlist'
    return create_item(request, PlayListForm, PlayList, 'core:playlist-songs', 'playlist_name', name)

@login_required
def newAlbum(request):
    if not request.user.verified:
        messages.error(request, 'You need to be a verified user to create an album.')
        return redirect('core:home')

    return create_item(request, AlbumForm, Album, 'core:album-songs', 'album_name')


@login_required
def addPlaylistSong(request, pk):
    return add_song(request, PlayList, pk, 'playlist', 'playlist', 'playlist-songs')

@login_required
def addAlbumSong(request, pk):
    return add_song(request, Album, pk, 'album', 'album', 'album-songs')


@login_required
def deleteSong(request, pk):
    song = get_object_or_404(Song, pk=pk)
    song.delete()

    return JsonResponse({'message': 'Song Deleted' })

@login_required
def deletePlaylist(request, pk):
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
