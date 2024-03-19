from . import views
from django.urls import path, include

app_name = 'exchange'

urlpatterns = [
    path('', views.index, name='index'),
]
