from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import PlayList, Song, User
from .forms import SignUpForm


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]

    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)

def songs(request, pk):
    songs = Song.objects.filter(playlist__id = pk)

    context = {'songs':songs}
    
    return render(request, 'core/songs.html', context)

# from django.contrib import messages

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