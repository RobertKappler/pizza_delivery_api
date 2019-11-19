FROM python:3.6
COPY pizza_delivery /
COPY Pipfile /
COPY Pipfile.lock /
RUN pip install pipenv
RUN pipenv install Pipfiles
CMD ["python", "pizza_delivery\manage.py", "makemigrations"]
CMD ["python", "pizza_delivery\manage.py", "migrations"]
CMD ["python", "pizza_delivery\manage.py", "runserver"]