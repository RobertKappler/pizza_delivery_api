import datetime

from rest_framework import serializers

from .models import Customer, Item, Orders


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model."""

    class Meta:
        model = Item
        fields = ['id', 'size', 'quantity', 'order_id', 'flavour', 'price']

    def create(self, validated_data):
        """Create an item object."""

        item = Item.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        """Update item instance with validated_data."""

        instance.size = validated_data.get('size', instance.size)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.flavour = validated_data.get('flavour', instance.flavour)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class OrdersSerializier(serializers.ModelSerializer):
    """Serializer for Orders model."""

    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = Orders
        fields = ['id', 'status', 'customer_id', 'items']

    def create(self, validated_data):
        """Create a new order under consideration of status and the need to create a customer and new items."""

        if 'customer' in validated_data.keys():
            customer_validated_data = validated_data.pop('customer')
            customer = Customer.objects.get(lastname=customer_validated_data['lastname'])
            if not customer:
                customer = Customer.objects.create(**customer_validated_data)
            validated_data['customer_id'] = customer['id']

        if not 'status' in validated_data.keys():
            validated_data['status'] = 0

        item_validated_data = validated_data.pop('items')
        validated_data['created_at'] = datetime.datetime.now()
        order = Orders.objects.create(**validated_data)

        for each in item_validated_data:
            each['order_id'] = order
            items = Item.objects.create(**each)

        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        items_data = validated_data.get('items', [])
        items = (instance.items).all()
        items = list(items)

        for item in items_data:
            order_item = items.pop(0)
            order_item.size = item.get('size', order_item.size)
            order_item.quantity = item.get('quantity', order_item.quantity)
            order_item.flavour = item.get('flavour', order_item.flavour)
            order_item.price = item.get('price', order_item.price)
            order_item.save()

        return instance


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrdersSerializier(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'lastname', 'name', 'address', 'orders']

    def create(self, validated_data):
        validated_data['created_at'] = datetime.datetime.now()
        return Customer.objects.create(**validated_data)
