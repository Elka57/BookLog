from django.urls import include, path
from . import views

app_name = 'account'      

urlpatterns = [
    path('api/', include('account.api.urls')),
]