from django.urls import include, path
from . import views
# from tutorial.quickstart import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'artworks', views.ArtworkViewSet)
# router.register(r'artworks', views.ArtworkViewSet)
# router.register(r'foo' , views.CurrentViewSet , base_name='artworks.Artwork')

urlpatterns = [
    path('foo/', views.foo, name='index'),
    path(r'list/', views.ListUsers.as_view()),
    path('', include(router.urls)),
]
