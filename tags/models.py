from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from django.contrib.staticfiles.templatetags.staticfiles import static

url = static('icon-user-default.png')


# USED FOR MODEL OF TAGS
class Tag(models.Model):
    streak = models.BigIntegerField(default = 0)
    name = models.CharField(max_length = 25, unique = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "owner")
    created = models.DateTimeField(default = timezone.now)
    original = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "original")
    def __str__(self):
        return self.name


# USED FOR GENERAL INFORMATION OF USER
class LoginUser(models.Model):
    username = models.CharField(max_length = 301)
    password = models.CharField(max_length = 300)


# USED FOR KEEPING TRACK OF FRIENDS
class Friendship(models.Model):
    created = models.DateTimeField(default = timezone.now)
    creator = models.ForeignKey(User, related_name = 'creator')
    friend = models.ForeignKey(User, related_name = 'friend')
    def __str__(self):
        return self.friend.username


# USED FOR OPTIONAL PROFILE INFORMATION
class Extra(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 300, blank = True)
    profileimage = models.ImageField( upload_to = "profilepics/", blank = True)
    def __str__(self):
        return self.user.username


# USED FOR KEEPING TRACK OF CREDITS
class Credits(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    credits = models.IntegerField(default = 100)
    def __str__(self):
        return self.user.username
