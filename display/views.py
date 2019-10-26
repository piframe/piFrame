from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader


def index(request):
    latest_question_list = ["artwork1", "artwork2"]
    template = loader.get_template('index.html')
    # template = loader.get_template('display/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
