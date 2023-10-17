from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),

	path('songs/<str:pk>', views.songs, name='songs'),
	path('addsong/<str:pk>', views.addSong, name='addsong'),

	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
 	path('signup/', views.signUp, name='signup'),

	path('new-playlist', views.createPlaylist, name='newplaylist'),
	path('delete-playlist/<str:pk>', views.deletePlaylist, name='deleteplaylist'),
	path('edit-playlist/<str:pk>', views.editPlaylist, name='editplaylist')
]
