from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'username',
            'first_name',
            'last_name'
        )
        model = models.User


class TagSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    original = UserSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'streak',
            'name',
            'owner',
            'created',
            'original'
        )
        model = models.Tag
