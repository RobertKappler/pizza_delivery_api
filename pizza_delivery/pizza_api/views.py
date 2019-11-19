from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .models import Orders, Customer
from .serializers import OrdersSerializier, CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


class OrderList(ListAPIView):
    """List all orders."""
    serializer_class = OrdersSerializier

    def get_queryset(self):
        """Define queryset to enabling filtering on customer_id and status."""

        queryset = Orders.objects.all()
        query_status = self.request.query_params.get('status', None)
        query_customer_id = self.request.query_params.get('customer_id', None)
        if query_status and query_customer_id:
            queryset = Orders.objects.filter(status=query_status,
                                             customer_id=query_customer_id)
        elif query_status:
            queryset = Orders.objects.filter(status=query_status)
        elif query_customer_id:
            queryset = Orders.objects.filter(customer_id=query_customer_id)
        return queryset


class OrderDetails(APIView):
    """Retrieve, update or delete an order."""

    @staticmethod
    def get_order(orderid):
        """Lookup if order details are available, based on orderid."""
        try:
            return Orders.objects.get(pk=orderid)
        except Orders.DoesNotExist:
            return None

    @staticmethod
    def get_order_by_customerid(customerid):
        """Lookup if order details are available, based on customerid."""

        try:
            return Orders.objects.get(customer_id=customerid)
        except Orders.DoesNotExist:
            return None
        except Orders.MultipleObjectsReturned:
            return True

    def get(self, request, orderid):
        """Retrieve order details."""
        order = self.get_order(orderid)
        serializer = OrdersSerializier(order)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request):
        """Update order details, all or partial."""

        all_data = request.data

        existing_order = None
        # check status of order if id is given
        if 'id' in all_data.keys():
            existing_order = self.get_order(all_data['id'])
            if existing_order.status > 1:
                return JsonResponse({'Error': 'Can`t change order details '
                                              'because the state of the '
                                              'delivery process too advanced'})

        # get customer_id out of customer details - create new or get existing
        elif 'customer' in all_data.keys():
            cus_data = all_data['customer']
            existing_cus = CustomerDetails().get_customer_by_name_and_address(
                cus_data['lastname'], cus_data['name'], cus_data['address'])
            if existing_cus:
                all_data['customer_id'] = existing_cus.id
            else:
                cus_serializer = CustomerSerializer(None, data=all_data[
                    'customer'], partial=True)
                if cus_serializer.is_valid():
                    saved_cus = cus_serializer.save()
                    all_data['customer_id'] = saved_cus.id

        # check its a new order and no customer information are provided
        elif 'customer_id' not in all_data.keys():
            return JsonResponse({'Error': 'Can`t create an order without any '
                                          'customer information are given. '
                                          'Please enter customer information '
                                          'or a customer_id.'})

        serializer = OrdersSerializier(existing_order, data=all_data,
                                       partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, orderid):
        """
        Delete order details and check if these is the last order for
        this customer.
        """

        order = self.get_order(orderid)
        if not self.get_order_by_customerid(order.customer_id):
            CustomerDetails().delete({}, order.customer_id)
        order.delete()
        return JsonResponse(status.HTTP_204_NO_CONTENT, safe=False)


class CustomerDetails(APIView):
    """Retrieve, update or delete an order."""

    @staticmethod
    def get_object(customerid):
        """Lookup if customer details are available, based on customerid."""

        try:
            return Customer.objects.get(pk=customerid)
        except Customer.DoesNotExist:
            raise Http404

    def get_customer_by_name_and_address(self, lastname, name, address):
        """
        Lookup if customer details are already available, based on
        lastname, name, address."""

        try:
            return Customer.objects.get(lastname=lastname, name=name,
                                        address=address)
        except Customer.DoesNotExist:
            return None

    def get(self, request, customerid):
        """Retrieve customer details."""

        customer = self.get_object(customerid)
        serialzier = CustomerSerializer(customer)
        return JsonResponse(serialzier.data, safe=False)

    def put(self, request, customerid):
        """Update customer details, all or partial."""

        customer = self.get_object(customerid)
        serializer = CustomerSerializer(customer, data=request.data,
                                        partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, customerid):
        """Delete customer details."""

        customer = self.get_object(customerid)
        customer.delete()
        return JsonResponse(status.HTTP_204_NO_CONTENT, safe=False)

    def post(self, request):
        """Insert new customer details."""

        lastname = request.data.get('lastname', None)
        name = request.data.get('name', None)
        address = request.data.get('address', None)
        customer = self.get_customer_by_name_and_address(lastname,
                                                         name, address)
        serializer = CustomerSerializer(customer,
                                        data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST, safe=False)
