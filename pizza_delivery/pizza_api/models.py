from django.db import models
import uuid

# Create your models here.


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lastname = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    address = models.CharField(max_length=150)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.name} {self.lastname}'


class Orders (models.Model):
    STATUS_CHOICES = [
        (0, 'Order received'),
        (1, 'Order will be processed'),
        (2, 'Order will be shipped'),
        (3, 'Order delivered'),
        (-1, 'Order canceled')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey(Customer, related_name='customer', on_delete=models.CASCADE)
    # status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.customer_id} - {self.status}'


class Item(models.Model):
    FLAVOUR_CHOICES = [
        ('margarita', 'Pizza Margarita'),
        ('marinara', 'Marinara Pizza'),
        ('salami', 'Salami Pizza')
    ]
    SIZE_CHOICES = [
        (26, 'Small - 26cm'),
        (28, 'Medium - 28cm'),
        (30, 'Large - 30cm'),
        (32, 'Extra large - 32cm')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    flavour = models.CharField(max_length=150, choices=FLAVOUR_CHOICES)
    quantity = models.IntegerField(default=1)
    size = models.IntegerField(choices=SIZE_CHOICES)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.order_id} - {self.quantity} - {self.size}'
