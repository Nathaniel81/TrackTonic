"""
Module for defining various forms for the Django application.

This module contains different forms that are used for user authentication, user management, playlist management,
song management, and album management within the application.
"""

# import os
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import authenticate

from .models import User, PlayList, Song, Album


class LoginForm(forms.Form):
    """
    A form for user login.

    Attributes:
        username (CharField): Field for entering the username.
        password (CharField): Field for entering the password.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')

    #     if username and password:
    #         user = authenticate(username=username, password=password)

    #         if not user:
    #             raise forms.ValidationError("User does not exist")
    #         if not user.check_password(password):
    #             raise forms.ValidationError("Incorrect Password")
    #         if not user.is_active:
    #             raise forms.ValidationError("Inactive User")
    #     return super(LoginForm, self).clean(*args, **kwargs)

class SignUpForm(UserCreationForm):
    """
    A form for user signup.

    Attributes:
        name (CharField): Field for entering a name.
        username (CharField): Field for entering username.
        email (EmailField): Field for entering email.
        password1 (CharField): Field for entering password.
        password2 (CharField): Field for entering password.
        otp (CharField): Field for entering the OTP.
    """
    otp = forms.CharField(max_length=6, label='Enter OTP', required=False)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2', 'otp')


class PlayListForm(forms.ModelForm):
    """
    A form for creating a new playlist.

    Attributes:
        playlist_name (CharField): Field for entering the playlist name.
        genre (CharField): Field for entering the genre of the playlist.
        cover (ImageField): Field for uploading the cover image of the playlist.
        description (CharField): Field for entering the description of the playlist.
    """
    class Meta:
        model = PlayList
        fields = ['playlist_name', 'genre', 'cover', 'description']

class NewSongForm(forms.ModelForm):
    """
    A form for adding a new song.

    Attributes:
        music_file (FileField): Field for uploading the music file.
    """
    class Meta:
        model = Song
        fields = ('music_file',)

# class NewSongForm(forms.Form):
#     song_name = forms.CharField(max_length=40)
#     music_files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))

#     def save_songs(self, playlist):
#         song_names = self.cleaned_data['song_name'].split(',')  # Assuming names are separated by commas
#         files = self.cleaned_data['music_files']

#         for i, file in enumerate(files):
#             if i < len(song_names):
#                 song = Song(song_name=song_names[i], music_file=file)
#             else:
#                 song = Song(song_name="Untitled", music_file=file)  # Default name if no name is provided

#             song.save()
#             playlist.songs.add(song)

class EditUserForm(forms.ModelForm):
    """
    A form for editing user details.

    Attributes:
        name (CharField): Field for entering the name of the user.
        username (CharField): Field for entering the username.
        email (EmailField): Field for entering the email of the user.
        avatar (ImageField): Field for uploading the avatar image of the user.
    """
    class Meta:
        model = User
        fields = ('name', 'username', 'email' ,'avatar',)

class AlbumForm(forms.ModelForm):
    """
    A form for creating a new album.

    Attributes:
        album_name (CharField): Field for entering the album name.
        genre (CharField): Field for entering the genre of the album.
        cover (ImageField): Field for uploading the cover image of the album.
        description (CharField): Field for entering the description of the album.
    """
    class Meta:
        model = Album
        fields = ('album_name', 'genre', 'cover', 'description',)
