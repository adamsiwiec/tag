from django import forms
from django.contrib.auth.forms import *
from .models import *

class UserCreate(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')

class LoginForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length = 301)
    password = forms.CharField(label = "Password", max_length = 300, widget=forms.PasswordInput)

    class Meta:
        model = LoginUser
        fields = ['username', 'password']

class TagForm(forms.ModelForm):
    name = forms.CharField(max_length = 25)
    class Meta:
        model = Tag
        fields = ['name']
class PassForm(forms.ModelForm):
    username = forms.CharField(max_length = 30)
    class Meta:
        model = LoginUser
        fields = ['username']
