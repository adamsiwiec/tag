from django import forms
from django.contrib.auth.forms import *
from .models import *

class UserCreate(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'e.g John'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'e.g Doe'}))
    email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'placeholder': 'johndoe@example.com'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email',]



class TagForm(forms.ModelForm):
    name = forms.CharField(max_length = 25, widget=forms.TextInput(attrs={'placeholder': 'e.g "Runner"', 'autofocus':'autofocus'}))
    class Meta:
        model = Tag
        fields = ['name']


class PassForm(forms.ModelForm):
    username = forms.CharField(max_length = 30)
    class Meta:
        model = LoginUser
        fields = ['username']


class FriendshipForm(forms.ModelForm):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    class Meta:
        model = Friendship
        fields = ['username']
