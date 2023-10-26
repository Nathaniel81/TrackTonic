from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
# from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Album, PlayList, Song, PlayListLike, AlbumLike, SongLike, User
from .forms import LoginForm, SignUpForm, PlayListForm, AlbumForm, NewSongForm, EditUserForm


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]
    albums = Album.objects.all().order_by('-created_at')[:20]
    query = request.GET.get('query', '')
    if query:
        playlists = PlayList.objects.filter(
            Q(playlist_name__icontains=query)| 
            Q(owner__username__icontains=query)| 
            Q(genre__icontains=query)|
            Q(description__icontains=query)|
            Q(songs__song_name=query)
        ).distinct()
        
    context = {'playlists':playlists, 'albums':albums}

    return render(request, 'core/index.html', context)

def get_user_data(request, username, template_name):
    user = User.objects.get(username=username)
    playlists = PlayList.objects.filter(owner=user)
    albums = Album.objects.filter(owner=user)
    context = {'user': user, 'playlists': playlists, 'albums': albums}
    return render(request, template_name, context)

def profile(request, username):
    return get_user_data(request, username, 'core/profile.html')

def library(request, username):
    return get_user_data(request, username, 'core/library.html')

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
def likePlaylist(request, pk):
    playlist = get_object_or_404(PlayList, pk=pk)
    liked = PlayListLike.objects.filter(user=request.user, playlist=playlist)
    
    if liked.exists():
        liked.delete()
    else:
        liked = PlayListLike.objects.create(user=request.user, playlist=playlist)
    return redirect('/')

@login_required
def likeAlbum(request, pk):
    album = get_object_or_404(Album, pk=pk)
    liked = AlbumLike.objects.filter(user=request.user, album=album)
    
    if liked.exists():
        liked.delete()
    else:
        liked = PlayListLike.objects.create(user=request.user, album=album)
    return redirect('/')

@login_required
def likeSong(request, pk):
    song = get_object_or_404(Song, pk=pk)
    liked = SongLike.objects.filter(user=request.user, song=song)
    
    if liked.exists():
        liked.delete()
    else:
        liked = SongLike.objects.create(user=request.user, song=song)
    return redirect('core:playlist-songs', pk=song.playlist.pk)
    

def playlistSongs(request, pk):
    name = 'playlist'
    playlist = PlayList.objects.get(pk=pk)
    # songs = Song.objects.filter(playlist__id = pk)
    songs = Song.objects.filter(content_type=ContentType.objects.get_for_model(playlist), object_id=pk)
    
    context = {'songs':songs, 'playlist':playlist, 'name': name}
    
    return render(request, 'core/songs.html', context)

def albumSongs(request, pk):
    album = Album.objects.get(pk=pk)
    # songs = Song.objects.filter(album__id = pk)
    songs = Song.objects.filter(content_type=ContentType.objects.get_for_model(album), object_id=pk)
    
    context = {'songs':songs, 'album':album}
    
    return render(request, 'core/songs.html', context)

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
            context = {'form': form}
            return render(request, 'core/new.html', context)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('core:playlist-songs', pk=playlist.pk)
    else:
        form = PlayListForm()

    context = {'form': form, 'Playlist': name}

    return render(request, 'core/new.html', context)

@login_required
def newAlbum(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        # name = form.cleaned_data['album_name']
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

def addPlaylistSong(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        if form.is_valid():
            newsong = form.save(commit=False)
            newsong.playlist = playlist
            newsong.content_type = ContentType.objects.get_for_model(PlayList)
            newsong.object_id = playlist.id
            newsong.save()
            return redirect('core:playlist-songs', pk=pk)
    form = NewSongForm()    
    context = {'form': form, 'playlist': playlist}    
    return render(request, 'core/add-songs.html', context)

def addAlbumSong(request, pk):
    album = Album.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        if form.is_valid():
            newsong = form.save(commit=False)
            newsong.album = album
            newsong.content_type = ContentType.objects.get_for_model(Album)
            newsong.object_id = album.id
            newsong.save()
            return redirect('core:album-songs', pk=pk)
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
        print("Post request")
        if form.is_valid():
            print("Valid")
            form.save()
            return redirect('core:playlist-songs', pk=pk)

    form = PlayListForm(instance=playlist)

    context = {'form': form, 'Playlist':name}

    return render(request, 'core/new.html', context)
