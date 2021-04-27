from django.urls import path

from . import views

urlpatterns = [
    path('get', views.get, name="get"),
    path('give', views.give, name="give"),
    path('get/item/<str:pk>', views.itemView, name="itemView"),
    path('get/<str:pk>', views.itemView, name="itemView"),
]
