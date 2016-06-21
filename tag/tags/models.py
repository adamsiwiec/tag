from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Tag(models.Model):
    streak = models.BigIntegerField(default = 0)
    name = models.CharField(max_length = 25, unique = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.name

class LoginUser(models.Model):
    username = models.CharField(max_length = 301)
    password = models.CharField(max_length = 300)

class Friendship(models.Model):
    created = models.DateTimeField(default = timezone.now)
    creator = models.ForeignKey(User, related_name = 'creator')
    friend = models.ForeignKey(User, related_name = 'friend')
    def __str__(self):
        return self.friend.username

class Extra(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 300)
    profileimage = models.ImageField( upload_to = "profilepics")
    def __str__(self):
        return self.user.username
