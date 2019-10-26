from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm
from django.template import loader
# from somewhere import handle_uploaded_file

# Imaginary function to handle an uploaded file.

from django.contrib.auth.models import User, Group
from artworks.models import Artwork

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'artworks/upload.html', {'form': form})


def index(request):
    latest_question_list = ["artwork1", "artwork2"]
    #template = loader.get_template('index.html')
    template = loader.get_template('artworks/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")
