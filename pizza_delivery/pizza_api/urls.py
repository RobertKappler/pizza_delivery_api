from django.urls import path

from . import views

urlpatterns = [
    #path('all_orders', views.retrieve_all_orders, name='retrieve_all_orders')
    path('orders/', views.orders_list)
]
