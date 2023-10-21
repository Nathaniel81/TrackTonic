from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import PlayList, Song, User, PlayListLike
from .forms import SignUpForm, PlayListForm, NewSongForm


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]
    query = request.GET.get('query', '')
    if query:
        playlists = PlayList.objects.filter(
            Q(playlist_name__icontains=query)| 
            Q(owner__username__icontains=query)| 
            Q(genre__icontains=query)|
            Q(description__icontains=query)|
            Q(songs__song_name=query)
        ).distinct()
        
    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)

def likepl(request, pk):
    playlist = get_object_or_404(PlayList, pk=pk)
    liked = PlayListLike.objects.filter(user=request.user, playlist=playlist)
    
    if liked.exists():
        liked.delete()
    else:
        liked = PlayListLike.objects.create(user=request.user, playlist=playlist)
    return redirect('/')
    

def songs(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    songs = Song.objects.filter(playlist__id = pk)
    
    context = {'songs':songs, 'playlist':playlist}
    
    return render(request, 'core/songs.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            message = 'Invalid username or password.'
            return render(request, 'core/login.html', {'message': message})
    
    return render(request, 'core/login.html')

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
    if request.method == 'POST':
        form = PlayListForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['playlist_name']
        existing_playlist = PlayList.objects.filter(playlist_name=name, owner=request.user)
        if existing_playlist:
            form.add_error('playlist_name', 'Playlist name already exists!')
            # print(form.errors)
            context = {'form': form}
            return render(request, 'core/newplaylist.html', context)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('core:songs', pk=playlist.pk)
    else:
        form = PlayListForm()
    context = {'form': form}
    return render(request, 'core/newplaylist.html', context)

@login_required
def addSong(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewSongForm(request.POST, request.FILES)
        if form.is_valid():
            newsong = form.save(commit=False)
            newsong.playlist = playlist
            newsong.save()
            return redirect('core:songs', pk=pk)
    form = NewSongForm()
    
    context = {'form': form, 'playlist': playlist}
    
    return render(request, 'core/addsongs.html', context)

@login_required
def deleteSong(request, pk):
    song = get_object_or_404(Song, pk=pk)
    playlist = PlayList.objects.get(pk=song.playlist.id)
    song.delete()

    return redirect('core:songs', pk=playlist.id)

@login_required
def deletePlaylist(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    playlist.delete()
    return redirect('/')

@login_required
def editPlaylist(request, pk):
    playlist = get_object_or_404(PlayList, pk=pk)
    if request.method == 'POST':
        form = PlayListForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('core:songs', pk=pk)

    form = PlayListForm(instance=playlist)

    context = {'form': form}

    return render(request, 'core/newplaylist.html', context)
    