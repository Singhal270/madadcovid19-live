from django.urls import path
from django.shortcuts import redirect
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
path('', RedirectView.as_view(url='/webhook')),
path('webhook/', views.webhook, name='webhook'),
path('add/', views.add, name='add'),
]