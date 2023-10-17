from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import PlayList, Song, User
from .forms import SignUpForm, NewPlayListForm, NewSongForm


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]

    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)

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
        form = NewPlayListForm(request.POST, request.FILES)
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
        form = NewPlayListForm()
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
def deletePlaylist(request, pk):
    playlist = PlayList.objects.get(pk=pk)
    playlist.delete()
    return redirect('/')
