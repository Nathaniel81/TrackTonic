from django.shortcuts import render
from .models import PlayList


def home(request):
    playlists = PlayList.objects.all().order_by('-created_at')[:20]

    context = {'playlists':playlists}

    return render(request, 'core/index.html', context)
