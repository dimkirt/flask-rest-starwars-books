## Description

Lohgarra, a Wookie from Kashyyyk, has a great idea. She wants to build a marketplace that allows her and her friends to
self-publish their adventures and sell them online to other Wookies. The profits would then be collected and donated to purchase
medical supplies for an impoverished Ewok settlement.

## Tasks

- Write a REST API using Python3, Flask and SQLAlchemy
- Implement a custom user model with a "author pseudonym" field
- Implement a book model. Each book should have a title, description, author, cover and price
- Provide an endpoint to authenticate with the API using username, password and return a JWT
- Provide an endpoint to publish books
- Provide endpoints to list all published books and retrieve single books
- Provide endpoints to search books by title
- Provide an endpoint that lists your own published books
- Provide an endpoint for unpublishing your own books
- Implement API tests for all endpoints
- Bonus: Make sure the user _Darth Vader_ is unable to publish his work on Wookie Books

## API docs

To document the API we use a published [Postman collection](https://documenter.getpostman.com/view/763923/SWLZgW7C?version=latest)

## Setup

Use [pyenv](https://github.com/pyenv/pyenv) to manage python versions and keep your working environment clean.

```bash
pyenv install 3.7.3
pyenv local 3.7.3
```

## Package Management

For package management we will use [pipenv](https://github.com/pypa/pipenv)

```bash
pip install pipenv
```

## Installation

```bash
pipenv install --dev
```

## Run Tests

Running the tests will create a test database and populate it with some test data.

```bash
pipenv run pytest
```

## Environmental Variables

These are the environmental variables we use, you can keep the defaults for testing

```bash
JWT_SECRET # defaults to: default-super-secret
DATABASE_URI # defaults to: sqlite:///../../wookie.sqlite.prod
```

## Setup local DB

To initialize migrations:

```bash
pipenv run python manage.py db init
pipenv run python manage.py db migrate
```

Note: The project already includes a migrations folder so you can skip the above commands.

To upgrade your local db in order to follow the migrations:

```bash
pipenv run python manage.py db upgrade
```

## Running the App

```bash
pipenv run gunicorn --workers 1 --bind 0.0.0.0:8000 wookie.wsgi:prod_app
```

## Running the App against test DB

In case you want to run the production app against the test database, in `wookie.wsgi.py` change this line:

```python
prod_app = app.create_app(config=config['production'])
```

to:

```python
prod_app = app.create_app(config=config['testing'])
```

```bash
pipenv run gunicorn --workers 1 --bind 0.0.0.0:8000 wookie.wsgi:prod_app
```
