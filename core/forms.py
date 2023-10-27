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
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2',)

class PlayListForm(forms.ModelForm):
    class Meta:
        model = PlayList
        fields = ['playlist_name', 'genre', 'cover', 'description']

class NewSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_name', 'music_file',)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email' ,'avatar',)

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('album_name', 'genre', 'cover', 'description',)
