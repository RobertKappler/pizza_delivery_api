from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Orders, Item, Customer
from .serializers import OrdersSerializier, ItemSerializer, CustomerSerializer


@csrf_exempt
def orders_list(request):
    """List all orders"""

    if request.method == 'GET':
        orders = Orders.objects.select_related().all()
        serializer = OrdersSerializier(orders, many=True)
        return JsonResponse(serializer.data, safe=False)




def index(request):
    return HttpResponse("HW")


def order_pizza(request, order, customer):
    # TODO get values out of order
    return HttpResponse(f'{order}')
# Create your views here.


def delete_order(request, id):
    # TODO lookup id and delete if possible
    return HttpResponse(f'{id} deleted')


def retrieve_order(request, id):
    # TODO lookup id and return informations
    order = id
    return HttpResponse(f'{order}')


def retrieve_all_orders(request):
    """"""
    # TODO return all orders
    # geht nicht
    all_order = Orders.objects.select_related().all()
    print(all_order[0].id)
    all_items = Item.objects.filter(order_id=all_order[0].id).all()
    print(all_items)
    #all_order = {}
    return HttpResponse(f'{all_order}')


def update_order(request, id, new_order_details):
    # TODO update just when not delivered/cooking
    # TODO check which details should be changed and change just them!
    updated_order = {}
    return HttpResponse(f'{updated_order}')
