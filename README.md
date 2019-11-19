# pizza_delivery_api
basic REST Api for a pizza delivery service. 

## Getting API running
This is just a short description to starts a lightweight development web server 
on the local machine to test the API functionality. If the API should be used in a production environment 
its recommended to use another web server. 
### Prerequisites
- Git (installed)
- Python 3.6 (installed)
- Postgresql 10 (running)


### Windows/ Linux/ MacOs
Use the following cmd commands to start the API locally. After this commands you can call the API via 
http://127.0.0.1:8000/pizza_api/{ENDPOINT}:
1. git clone https://github.com/RobertKappler/pizza_delivery_api.git
2. cd pizza_delivery_api
3. pip install pipenv
4. pipenv install Pipfile
5. cd pizza_delivery
6. pipenv run python manage.py makemigrations
7. pipenv run python manage.py migrate
8. pipenv run python manage.py runserver

## Endpoints

### List orders
URL: {SERVER_ADDRESS}/pizza_api/orders   
Method: GET   
if you want to filter against 'customer_id' or 'status' of an order, use it as query_parameter

### Retrieve order
URL: {SERVER_ADDRESS}/pizza_api/order/{ORDER_ID}   
Method: GET

### DELETE order
URL: {SERVER_ADDRESS}/pizza_api/order/{ORDER_ID}   
Method: DELETE

### Update order
URL: {SERVER_ADDRESS}/pizza_api/order   
Method: PUT   
Body-type: Json   

An order can just get updated if the 'status' is below 2. 

### Declaration of placeholder dictionaries
To avoid long strings in response or in the request body following choices were defined in the model.    

    STATUS_CHOICES = [
        (0, 'Order received'),
        (1, 'Order will be processed'),
        (2, 'Order will be shipped'),
        (3, 'Order delivered')
    ]
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