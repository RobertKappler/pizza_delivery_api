from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.orders_list),
    path('customer_details/<uuid:customer_id>/', views.customer_details),
    path('remove_order/<uuid:order_id>/', views.remove_order),
    path('insert_order/', views.insert_order)
]
