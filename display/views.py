# from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import loader
from django.conf import settings


def index(request):
    template = loader.get_template('index.html')
    # template = loader.get_template('display/index.html')

    portrait = False
    if settings.DISPLAY_ROTATE:
        display_rotate = int(settings.DISPLAY_ROTATE)
        if display_rotate == 1 or display_rotate == 3:
            portrait = True

    context = {
        'display_rotate': settings.DISPLAY_ROTATE,
        'rpi_hostname': settings.RPI_HOSTNAME,
        'rpi_ip': settings.RPI_IP,
        'portrait': portrait,
    }
    return HttpResponse(template.render(context, request))
