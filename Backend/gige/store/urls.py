from django.urls import path

from . import views

urlpatterns = [
    path('get/', views.get, name="get"),
    path('get/item/<str:pk>/', views.itemView, name="itemView"),
    path('get/<str:pk>/', views.categoryView, name="categoryView"),
    path('get/item/<str:pk>/buy/', views.itemBuy, name="itemBuy"),
    path('get/search/<str:pk>', views.itemSearch, name="itemSearcf"),
    path('give/', views.give, name="give"),
    path('give/add/', views.itemAdd, name="itemAdd"),
    # path('give/<str:pk>/', views.giveItem, name="giveItem"),
    path('give/edit/<str:pk>/', views.itemEdit, name="itemEdit"),
    path('give/delete/<str:pk>/', views.itemDelete, name="itemDelete"),
    path('give/todoadd/', views.Todoadd, name="Todoadd"),
    path('give/tododelete/<str:pk>', views.Tododelete, name="Tododelete"),
]
