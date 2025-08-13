from django.urls import include, path
from . import views

app_name = 'users'      

urlpatterns = [
    path('', include('users.api.urls')),
]