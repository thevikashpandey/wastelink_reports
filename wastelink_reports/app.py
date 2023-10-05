# appname/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
# appname/views.py

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, this is your homepage!')
# appname/views.py

