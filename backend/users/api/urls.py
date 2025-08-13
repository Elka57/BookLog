from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import ProfileDeleteViewSet, UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'profile-delete', ProfileDeleteViewSet, basename='profile-delete')


urlpatterns = [
    path('', include(router.urls)),
]
