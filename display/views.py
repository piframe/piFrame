# from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import loader
from django.conf import settings


def index(request):
    latest_question_list = ["artwork1", "artwork2"]
    template = loader.get_template('index.html')
    # template = loader.get_template('display/index.html')

    portrait = False
    if settings.DISPLAY_ROTATE:
        display_rotate = int(settings.DISPLAY_ROTATE)
        if display_rotate == 1 or display_rotate == 3:
            portrait = True

    context = {
        'latest_question_list': latest_question_list,
        'display_rotate': settings.DISPLAY_ROTATE,
        'portrait': portrait,
        'foo': 'bar',
    }
    return HttpResponse(template.render(context, request))
