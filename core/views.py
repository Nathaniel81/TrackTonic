from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import PlayList, Song, User
from .forms import SignUpForm, NewPlayListForm


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]

    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)

def songs(request, pk):
    songs = Song.objects.filter(playlist__id = pk)

    context = {'songs':songs}
    
    return render(request, 'core/songs.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'core/login.html')

def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('core:home')
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
