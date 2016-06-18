from django.db import models


class Tag(models.Model):
    streak = models.BigIntegerField()
    name = models.CharField(max_length = 25, unique = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
