from django.shortcuts import render, get_object_or_404
from .models import PlayList, Song


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]

    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)

def songs(request, pk):
    songs = Song.objects.filter(playlist__id = pk)
    context = {'songs':songs}
    
    return render(request, 'core/songs.html', context)
