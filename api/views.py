# from rest_framework import status
from rest_framework.decorators import api_view
# from django.shortcuts import render
# Create your views here.
# from django.http import HttpResponseRedirect, HttpResponse
# from django.template import loader
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from django.http import JsonResponse
# from somewhere import handle_uploaded_file

# Imaginary function to handle an uploaded file.
from django.contrib.auth.models import User, Group
from artworks.models import Artwork
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArtworkSerializer

from django.conf import settings

import subprocess


@api_view(['GET'])
def foo(request, format=None):
    configs = settings.RPI_CONFIGS
    theip = settings.RPI_IP

    content = {
        'pi_configs': configs,
        'display_rotate': settings.DISPLAY_ROTATE,
        'pi_config_file': settings.RASBIAN_CONFIG_PATH,
        'configparser_config_file': settings.SETTINGS_FILE_PATH,
        'theip': theip
    }
    return Response(content)
    # return Response(content, template_name='articles.html')
    # return JsonResponse(content)


@api_view(['GET'])
def display_power(request, format=None):
    try:
        proc = subprocess.Popen(['vcgencmd', 'display_power'], stdout=subprocess.PIPE)
        output = proc.stdout.read()
    except:
        output = "display_power=-1\n"

    name, value = output.split("=")

    content = {
        name: int(value.strip()),
    }
    return Response(content)


@api_view(['POST'])
def display_power_set(request, state=1, format=None):
    # output = "display_power=-1\n"

    if state == 1 or state == '1' or state == 'on':
        proc = subprocess.Popen(['vcgencmd', 'display_power', '1'], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        name = 'on'

    if state == 0 or state == '0' or state == 'off':
        proc = subprocess.Popen(['vcgencmd', 'display_power', '0'], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        name = 'off'

    #  name, value = output.split("=")

    content = {
        'name': name,
        'state': state,
    }
    return Response(content)


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


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
