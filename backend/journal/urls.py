from django.urls import include, path
from . import views

app_name = 'journal'      

urlpatterns = [
    path('', include('journal.api.urls')),
]