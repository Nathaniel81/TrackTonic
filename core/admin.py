from django.contrib import admin
from .models import User, Playlist, Song, Album, PlaylistLike, AlbumLike, SongLike, Genre

admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(PlaylistLike)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(AlbumLike)
admin.site.register(SongLike)
admin.site.register(Genre)
