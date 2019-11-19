from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrderList.as_view(), name='orders'),
    path('order/<uuid:orderid>', views.OrderDetails.as_view()),
    path('order', views.OrderDetails.as_view(), name='order')
]
