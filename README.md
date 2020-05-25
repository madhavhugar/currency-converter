# Currency-converter

![Python](https://img.shields.io/badge/python-v3.6-blue)

Django application for currency conversion

## Setup instructions

### Run locally

- Setup virtualenv using `Pipenv` or `venv` (using `python_version = "3.6"`)

#### Pipenv

- Install Pipenv 

```
  pipenv install
  pipenv shell
  python manage.py runserver
```

#### venv

- Create venv and activate it

```
  pip install -r requirements.txt
  python manage.py runserver
```

### Run in Container

- Install `docker` & `docker-compose`

```
  docker-compose up
```

Access the application on `localhost:8000`

## Tests

Execute tests 

```
  python manage.py test
```
## Sample requests

```
GET => /convert/?amount=20.0&reference_date=2020-05-20&src_currency=EUR&dest_currency=GBP

{
  "amount": 17.87,
  "currency": "GBP",
}
```
