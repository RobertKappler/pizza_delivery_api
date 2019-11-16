from rest_framework import serializers

from .models import Customer, Item, Orders


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'size', 'quantity', 'order_id', 'flavour', 'price']


class OrdersSerializier(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'status', 'customer_id', 'items']


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrdersSerializier(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'lastname', 'name', 'age', 'address', 'orders']
