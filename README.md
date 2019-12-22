## Flask - Wookie Books

### Description

Lohgarra, a Wookie from Kashyyyk, has a great idea. She wants to build a marketplace that allows her and her friends to
self-publish their adventures and sell them online to other Wookies. The profits would then be collected and donated to purchase
medical supplies for an impoverished Ewok settlement.

### Tasks

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

### Evaluation Criteria

- Follow best practices when working with settings, apps, models and authentication
- Write API tests for all implemented endpoints
- Make sure that users may only unpublish their own books
- Bonus: Make sure the user _Darth Vader_ is unable to publish his work on Wookie Books

### Useful Links

[Flask](https://palletsprojects.com/p/flask/)
[SQLAlchemy](https://docs.sqlalchemy.org/)

### CodeSubmit

Please organize, design, test and document your code as if it were
going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The CodeSubmit Team

## Running the App

```bash
pipenv run gunicorn --workers 1 --bind 0.0.0.0:8000 wookie.wsgi:prod_app
```
