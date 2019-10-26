from django.urls import include, path
from . import views
# from tutorial.quickstart import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'artworks', views.ArtworkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
