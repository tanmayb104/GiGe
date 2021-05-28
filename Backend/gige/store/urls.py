from django.urls import path

from . import views

urlpatterns = [
    path('get/', views.get, name="get"),
    path('get/item/<str:pk>/', views.itemView, name="itemView"),
    path('get/category/<str:pk>/', views.categoryView, name="categoryView"),
    path('get/item/<str:pk>/buy/', views.itemBuy, name="itemBuy"),
    path('get/search/', views.itemSearch, name="itemSearch"),
    path('get/orders/', views.getOrders, name="getOrders"),
    path('get/orders/<str:pk>', views.DeleteGetOrders, name="DeleteGetOrders"),
    path('give/', views.give, name="give"),
    path('give/add/', views.itemAdd, name="itemAdd"),
    path('give/edit/<str:pk>/', views.itemEdit, name="itemEdit"),
    path('give/delete/<str:pk>/', views.itemDelete, name="itemDelete"),
    path('give/todoadd/', views.Todoadd, name="Todoadd"),
    path('give/tododelete/<str:pk>', views.Tododelete, name="Tododelete"),
    path('give/orders/', views.giveOrders, name="giveOrders"),
    path('give/orders/<str:pk>', views.DeleteGiveOrders, name="DeleteGiveOrders"),
]
