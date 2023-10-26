from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),

	path('playlist/songs/<str:pk>', views.playlistSongs, name='playlist-songs'),
	path('album/songs/<str:pk>', views.albumSongs, name='album-songs'),

	path('add-playlist-song/<str:pk>', views.addPlaylistSong, name='addsongPl'),
	path('add-album-song/<str:pk>', views.addAlbumSong, name='addsongAl'),
 
	path('delete-song/<str:pk>', views.deleteSong, name='deletesong'),

	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
 	path('signup/', views.signUp, name='signup'),
  
	path('@<str:username>/', views.profile, name='profile'),
	path('@<str:username>/library', views.library, name='library'),
	path('@<str:username>/edit', views.editProfile, name='editprofile'),

	path('new-playlist', views.createPlaylist, name='newplaylist'),
 	path('new-album', views.newAlbum, name='new-album'),
	path('delete-playlist/<str:pk>', views.deletePlaylist, name='deleteplaylist'),
	path('edit-playlist/<str:pk>', views.editPlaylist, name='editplaylist'),
 
	path('like-playlist/<str:pk>', views.likePlaylist, name='likeplaylist'),
	path('like-album/<str:pk>', views.likeAlbum, name='likealbum'),
	path('like-song/<str:pk>', views.likeSong, name='likesong'),
]
