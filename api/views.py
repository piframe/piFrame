from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
# from somewhere import handle_uploaded_file

# Imaginary function to handle an uploaded file.

from django.contrib.auth.models import User, Group
from artworks.models import Artwork
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArtworkSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArtworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
