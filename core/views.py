from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from django.core.files.base import ContentFile

from datetime import timedelta
from django.utils import timezone

from .models import Album, PlayList, Song, PlayListLike, AlbumLike, SongLike, User
from .forms import LoginForm, SignUpForm, PlayListForm, AlbumForm, NewSongForm, EditUserForm


def home(request):
    current_time = timezone.now().time()
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

def get_user_data(request, username, template_name):
    user = User.objects.get(username=username)
    playlists = PlayList.objects.filter(owner=user)[:10]
    liked_playlists =  PlayListLike.objects.filter(user=request.user)[:10]
    liked_albums =  AlbumLike.objects.filter(user=request.user)[:10]
    # for obj in liked_playlists:
    #     print(obj.__dict__)
    # print(liked_playlists[0].__dict__['_state'].__str__())
    # print(str(liked_playlists[0]._state))

    albums = Album.objects.filter(owner=user)[:10]
    context = {
        'user': user, 
        'playlists': playlists, 
        'albums': albums, 
        'liked_playlists': liked_playlists, 
        'liked_album':liked_albums
        }
    return render(request, template_name, context)

def profile(request, username):
    return get_user_data(request, username, 'core/profile.html')

def library(request, username):
    return get_user_data(request, username, 'core/library.html')

@login_required
def liked(request):
    user = get_object_or_404(User, id=request.user.id)
    return get_user_data(request, user.username, 'core/liked.html')
    

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
    is_liked = False
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        playlist_id = request.POST.get('playlist_id')
        playlist = get_object_or_404(PlayList, pk=playlist_id)
        liked = PlayListLike.objects.filter(user=request.user, playlist=playlist)
        if liked.exists():
            liked.delete()
        else:
            liked = PlayListLike.objects.create(user=request.user, playlist=playlist)
            is_liked = True
        likes_count = playlist.playlist_likes.count()
        return JsonResponse({'likes_count': likes_count, 'is_liked': is_liked})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def likeAlbum(request, pk):
    album = get_object_or_404(Album, pk=pk)
    liked = AlbumLike.objects.filter(user=request.user, album=album)
    
    if liked.exists():
        liked.delete()
    else:
        liked = PlayListLike.objects.create(user=request.user, name=album.owner.name, album=album)
    return redirect('/')

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

def playlistSongs(request, name, pk):
    playlist = get_object_or_404(PlayList, pk=pk)
    songs = list(Song.objects.filter(content_type=ContentType.objects.get_for_model(playlist), object_id=pk))

    is_liked = False
    # newSongs = []

    if request.user.is_authenticated:
        is_liked = playlist.playlist_likes.filter(user=request.user).exists()
        # newSongs = [song.id for song in songs if song.song_likes.filter(user=request.user).exists()]
    liked_songs = []    
    for song in songs:
        if song.song_likes.filter(user=request.user).exists():
            # print("Found Liked Song: ", song.id)
            liked_songs.append(song)
    print(liked_songs)
    print(songs)
    print(type(liked_songs), type(songs))
    context = {
        'songs': songs,
        'playlist': playlist,
        'name': name,
        'playlist_id': pk,
        'is_liked': is_liked,
        'liked_songs': liked_songs
        # 'newSongs': newSongs
    }
    return render(request, 'core/playlist-songs.html', context)

def albumSongs(request, name, pk):
    album = Album.objects.get(pk=pk)
    # songs = Song.objects.filter(album__id = pk)
    songs = Song.objects.filter(content_type=ContentType.objects.get_for_model(album), object_id=pk)
    
    context = {'songs':songs, 'album':album}
    
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
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('core:home')
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
    if request.method == 'POST':
        form = PlayListForm(request.POST, request.FILES)
        name = form.data.get('playlist_name')
        existing_playlist = PlayList.objects.filter(playlist_name=name, owner=request.user)
        
        if existing_playlist.exists():
            form.add_error('playlist_name', 'Playlist name already exists!')
            context = {'form': form, 'playlist': name}
            return render(request, 'core/new.html', context)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('core:playlist-songs', name=request.user.name, pk=playlist.pk)
    else:
        form = PlayListForm()

    context = {'form': form, 'Playlist': name}

    return render(request, 'core/new.html', context)

@login_required
def newAlbum(request):
    if not request.user.verified:
        messages.error(request, 'You need to be a verified user to create an album.')
        return redirect('core:home')

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        name = form.data.get('album_name')
        existing_album = Album.objects.filter(album_name=name, owner=request.user)
    
        if existing_album:
            form.add_error('album_name', 'Album name already exists!')
            # print(form.errors)
            context = {'form': form}
            return render(request, 'core/new.html', context)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect('core:album-songs', pk=album.pk)
    else:
        form = AlbumForm()
    context = {'form': form}

    return render(request, 'core/new.html', context)


def get_song_attributes(song, playlist):
    audio = EasyID3(song.temporary_file_path())
    artist_name = audio.get('artist', ['Unknown artist'])[0]

    song_name = song.name
    duration = MP3(song.temporary_file_path()).info.length
    total_seconds = int(duration)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    duration_string = f"{minutes}:{seconds:02}"

    audio_tags = ID3(song.temporary_file_path())
    cover_image = None
    if 'APIC:' in audio_tags:
        for key in audio_tags.keys():
            if key.startswith('APIC:'):
                picture = audio_tags[key]
                cover_image = ContentFile(picture.data)

    return {
        'song_name': song_name,
        'artist_name': artist_name,
        'duration': duration_string,
        'cover_image': cover_image,
        'playlist': playlist,
    }


def addPlaylistSong(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        musicFiles = request.FILES.getlist('music_file')
        if form.is_valid():
            for music in musicFiles:
                newsong = Song(content_object=playlist)
                newsong.music_file = music
                newsong.playlist = playlist #functioning as a custom attribute to generate the upload path.
                newsong.content_type = ContentType.objects.get_for_model(PlayList)
                newsong.object_id = playlist.id

                song_attributes = get_song_attributes(music, playlist)
                newsong.song_name = song_attributes['song_name']
                newsong.artist_name = song_attributes['artist_name']
                newsong.duration = song_attributes['duration']
                newsong.cover_image.save(f"{music.name}_cover.jpg", song_attributes['cover_image'], save=True)

                newsong.save()
            return redirect('core:playlist-songs', name=playlist.owner.name, pk=pk)
    else:
        form = NewSongForm()
    context = {'form': form, 'playlist': playlist}
    return render(request, 'core/add-songs.html', context)

def addAlbumSong(request, pk):
    album = Album.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        musicFiles = request.FILES.getlist('music_file')
        if form.is_valid():
            for music in musicFiles:
                new_song = Song(content_object=album)
                new_song.music_file = music
                new_song.album = album #functioning as a custom attribute to generate the upload path.
                new_song.content_type = ContentType.objects.get_for_model(Album)
                new_song.object_id = album.id

                song_attributes = get_song_attributes(music, album)
                new_song.song_name = song_attributes['song_name']
                new_song.artist_name = song_attributes['artist_name']
                new_song.duration = song_attributes['duration']
                new_song.cover_image.save(f"{music.name}_cover.jpg", song_attributes['cover_image'], save=True)

                new_song.save()
            return redirect('core:album-songs', name=album.artist.name, pk=pk)
    else:
        form = NewSongForm()
    context = {'form': form, 'album': album}
    return render(request, 'core/add-songs.html', context)

@login_required
def deleteSong(request, pk):
    song = get_object_or_404(Song, pk=pk)
    playlist = PlayList.objects.get(pk=song.playlist.id)
    song.delete()

    return redirect('core:playlist-songs', pk=playlist.id)

@login_required
def deletePlaylist(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    playlist.delete()
    return redirect('/')

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
