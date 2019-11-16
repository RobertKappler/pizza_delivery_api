from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Orders, Item, Customer
from .serializers import OrdersSerializier, ItemSerializer, CustomerSerializer


@csrf_exempt
def orders_list(request):
    """List all orders."""

    if request.method == 'GET':
        orders = Orders.objects.select_related().all()
        serializer = OrdersSerializier(orders, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def customer_details(request, customer_id):
    """Retrieve specific customer details."""

    if request.method == 'GET':
        customer = Customer.objects.select_related().get(pk=customer_id)
        serializer = CustomerSerializer(customer, many=False)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def insert_order(request):
    """Insert a new order."""
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OrdersSerializier(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def remove_order(request, order_id):
    if request.method == 'POST':
        order = Orders.objects.select_related().get(pk=order_id)
        print(order)
        serializer = OrdersSerializier(order, many=False)
        return JsonResponse(serializer.data, safe=False)


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
