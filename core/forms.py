from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2',)
