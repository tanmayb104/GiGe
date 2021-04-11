from django.urls import path

from . import views

urlpatterns = [
    path('mode', views.mode, name="mode"),
]
