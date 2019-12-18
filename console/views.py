from django.shortcuts import render
from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import loader
from django.conf import settings


def index(request):
    template = loader.get_template('dindex.html')

    context = {
        'x': 'x',
    }

    return HttpResponse(template.render(context, request))
