from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),

	path('songs/<str:pk>', views.songs, name='songs'),
	path('addsong/<str:pk>', views.addSong, name='addsong'),
	path('delete-song/<str:pk>', views.deleteSong, name='deletesong'),

	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
 	path('signup/', views.signUp, name='signup'),
  
	path('@<str:username>/', views.profile, name='profile'),
	path('@<str:username>/edit', views.editProfile, name='editprofile'),

	path('new-playlist', views.createPlaylist, name='newplaylist'),
	path('delete-playlist/<str:pk>', views.deletePlaylist, name='deleteplaylist'),
	path('edit-playlist/<str:pk>', views.editPlaylist, name='editplaylist'),
 
	path('like-playlist/<str:pk>', views.likePlaylist, name='likeplaylist'),
	path('like-album/<str:pk>', views.likeAlbum, name='likealbum'),
	path('like-song/<str:pk>', views.likeSong, name='likesong'),
]
