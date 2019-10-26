from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from tutorial.quickstart import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='Upload Files'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
