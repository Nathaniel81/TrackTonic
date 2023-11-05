import os
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

from .models import User, PlayList, Song, Album


class LoginForm(forms.Form):
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
    otp = forms.CharField(max_length=6, label='Enter OTP', required=False)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2', 'otp')


class PlayListForm(forms.ModelForm):
    class Meta:
        model = PlayList
        fields = ['playlist_name', 'genre', 'cover', 'description']

class NewSongForm(forms.ModelForm):
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
    class Meta:
        model = User
        fields = ('name', 'username', 'email' ,'avatar',)

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('album_name', 'genre', 'cover', 'description',)
