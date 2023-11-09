"""
context processor for genre objects
"""

from .models import Genre

def genre_context(request):
    genres = Genre.objects.all()
    return {'genres': genres}
