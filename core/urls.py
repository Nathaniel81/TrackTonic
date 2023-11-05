from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),

	path('@<str:name>/playlist/<str:pk>', views.playlistSongs, name='playlist-songs'),
	path('@<str:name>/album/<str:pk>', views.albumSongs, name='album-songs'),

	path('add-playlist-song/<str:pk>', views.addPlaylistSong, name='addsongPl'),
	path('add-album-song/<str:pk>', views.addAlbumSong, name='addsongAl'),
	path('download/<int:song_id>/', views.download_song, name='download_song'),
	path('download-playlist/<int:pk>/', views.download_playlist, name='download_playlist'),
	path('download-album/<int:pk>/', views.download_album, name='download_album'),
	# path('download/<int:song_id>/<int:pl_id>', views.download_song_with_watermark, name='download_song'),
 
	path('delete-song/<str:pk>', views.deleteSong, name='deletesong'),

	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
 	path('signup/', views.signUp, name='signup'),
  
	path('@<str:username>/', views.profile, name='profile'),
	path('@<str:username>/library', views.library, name='library'),
	path('@<str:username>/edit', views.editProfile, name='edit-profile'),

	path('new-playlist', views.createPlaylist, name='newplaylist'),
 	path('new-album', views.newAlbum, name='new-album'),
	path('delete-playlist/<str:pk>', views.deletePlaylist, name='deleteplaylist'),
	path('edit-playlist/<str:pk>', views.editPlaylist, name='editplaylist'),
 
	path('like-playlist/', views.likePlaylist, name='likeplaylist'),
	path('like-album/', views.likeAlbum, name='likealbum'),
	path('like-song/<str:pk>', views.likeSong, name='likesong'),
 
	path('liked/', views.liked, name='liked'),
	path('isliked/<int:pk>', views.isLiked, name='isliked')
 
]
