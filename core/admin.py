from django.contrib import admin
from .models import User, PlayList, Song

admin.site.register(User)
admin.site.register(PlayList)
admin.site.register(Song)

