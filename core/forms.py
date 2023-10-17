from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, PlayList

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2',)

class NewPlayListForm(forms.ModelForm):
    class Meta:
        model = PlayList
        fields = ['playlist_name', 'genre', 'cover', 'description']
