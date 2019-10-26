from django.contrib.auth.models import User, Group
from artworks.models import Artwork
from rest_framework import serializers
# from PIL import Image


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArtworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artwork
        fields = ['photo', 'url', 'landscape', 'portrait']
