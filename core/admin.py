from django.contrib import admin
from .models import User, PlayList, Song, Album, AlbumLike, PlayListLike, SongLike

admin.site.register(User)
admin.site.register(PlayList)
admin.site.register(PlayListLike)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(AlbumLike)
admin.site.register(SongLike)

