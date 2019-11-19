from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from pizza_api.models import Orders


class OrderTests(APITestCase):
    fixtures = ['fixture.json']

    def test_get_order_list(self):
        """
            Define a test for endpoint orders and check if it return
            a status_code 200 and a list as date type
        """
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], '0247c292-63b0-4395-ae11-f60241680244')

    def test_put_order(self):
        """
            Define a test which enter a new order to the customer of the fixture.
        """
        url = reverse('order')
        data = {
                "customer_id": "63e11a27-60f6-4815-9c18-b9e348588d91",
                "status": 1,
                "items": [{
                    "flavour": "margarita",
                    "qty": 3,
                    "size": 26
                    }]
                }
        # check amount of orders before put a new order
        self.assertEqual(Orders.objects.count(), 1)

        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Orders.objects.count(), 2)
