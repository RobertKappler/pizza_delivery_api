from rest_framework import serializers

from .models import Customer, Item, Orders


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'size', 'quantity', 'order_id', 'flavour']


class OrdersSerializier(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'status', 'items', 'created_at']


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrdersSerializier(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'lastname', 'name', 'age', 'address', 'orders', 'created_at']
