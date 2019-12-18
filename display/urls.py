from django.urls import include, path
from display import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
