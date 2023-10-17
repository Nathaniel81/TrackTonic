from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.home, name='home'),
	path('songs/<str:pk>', views.songs, name='songs'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
 	path('signup/', views.signUp, name='signup'),
	path('newplaylist', views.createPlaylist, name='newplaylist'),
]
