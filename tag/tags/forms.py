from django import forms
from django.contrib.auth.forms import *
from .models import *


# CREATES A NEW USER
class UserCreate(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' John'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' Doe'}))
    email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'placeholder': ' johndoe@example.com'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email',]
    def __init__(self, *args, **kwargs):
        super(UserCreate, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

# CREATES A TAG
class TagForm(forms.ModelForm):
    name = forms.CharField(max_length = 25, widget=forms.TextInput(attrs={'placeholder': 'e.g "Runner"', 'autofocus':'autofocus'}))
    class Meta:
        model = Tag
        fields = ['name']


# PASSES ON A TAG
class PassForm(forms.ModelForm):
    username = forms.CharField(max_length = 30)
    class Meta:
        model = LoginUser
        fields = ['username']


# CREATES A NEW FRIEND
class FriendshipForm(forms.ModelForm):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    class Meta:
        model = Friendship
        fields = ['username']


# ADDS EXTRA PROFILE INFORMATION
class ExtraForm(forms.ModelForm):
    bio = forms.CharField(max_length = 300, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    profileimage = forms.ImageField()
    class Meta:
        model = Extra
        fields = ['bio', 'profileimage']
