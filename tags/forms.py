from django import forms
from django.contrib.auth.forms import *
from .models import *
import re
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

def valid_tag(tag):
    if re.search(r"[0-9\\/_0-9\!@#\$%&\*'\[\]\}\{\?:;\.,<>\=\+\-\)\(\^`~\|]", tag):
        raise ValidationError(_("Please don't use numbers or symbols"))

# LOG IN USER
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=300,widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'col-lg-8  col-lg-offset-2'
    helper.layout = Layout(
        'username',
        'password',
        FormActions(Submit('Login', 'Login', css_class="btn-primary"))

    )


# CREATES A NEW USER
class UserCreate(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' John'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' Doe'}))
    email = forms.EmailField(max_length=75,label = "Email", widget=forms.TextInput(attrs={'placeholder': ' johndoe@example.com'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email',]
    def __init__(self, *args, **kwargs):
        super(UserCreate, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'col-lg-8  col-lg-offset-2'
    helper.layout = Layout(
        'first_name',
        'last_name',
        'username',
        'email',
        'password1',
        'password2',
        FormActions(Submit('Create', 'Create', css_class="btn-primary"))

    )

# CREATES A TAG
class TagForm(forms.ModelForm):
    name = forms.CharField(max_length = 25,validators = [valid_tag], widget=forms.TextInput(attrs={'placeholder': 'e.g "Runner"', 'autofocus':'autofocus'}))
#
    class Meta:
        model = Tag
        fields = ['name']
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Create', 'Create', css_class="btn-primary"))


# PASSES ON A TAG
class PassForm(forms.ModelForm):
    username = forms.CharField(max_length = 30)
    class Meta:
        model = LoginUser
        fields = ['username']
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'col-lg-8  col-lg-offset-2'
    helper.layout = Layout(
        'username',
        FormActions(Submit('Pass', 'Pass', css_class="btn-primary"))

    )


# CREATES A NEW FRIEND
class FriendshipForm(forms.ModelForm):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    class Meta:
        model = Friendship
        fields = ['username']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'col-lg-8  col-lg-offset-2'
    helper.layout = Layout(
        'username',
        FormActions(Submit('Add', 'Add', css_class="btn-primary"))

    )


# ADDS EXTRA PROFILE INFORMATION
class ExtraForm(forms.ModelForm):
    bio = forms.CharField(max_length = 300, required = False,  widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    profileimage = forms.ImageField(required = False)
    class Meta:
        model = Extra
        fields = ['bio', 'profileimage']

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'col-lg-8  col-lg-offset-2 m-y-3'
    helper.layout = Layout(
        'bio',
        'profileimage',
        FormActions(Submit('Submit', 'Submit', css_class="btn-primary"))

    )
