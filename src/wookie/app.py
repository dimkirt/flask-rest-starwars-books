from flask import Flask
from flask_restful import Api

import flask_jwt_extended

from . import utils
from .books import resources as book_resources
from .books.dao import BooksDAO
from .auth import resources as auth_resources
from .users.dao import UsersDAO


def create_app():
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # TODO: Move this to env var

    api = Api(app)
    flask_jwt_extended.JWTManager(app)

    app_logger = utils.create_logger(__name__)
    # Use in-memory storage for now
    db = {
        'books': [{
            'id': 0,
            'title': 'This is the title',
            'author': 'This is the author',
            'description': 'This is the description',
            'price': 100,
            'cover':
            'https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/220px-Lenna_%28test_image%29.png',  # noqa
            'publisher': 0,  # id of the publisher
        }],
        'users': [{
            'id': 0,
            'username': 'jedi-master',
            'password': 'Test1234',
            'author_pseudonym': 'Luke'
        }]
    }

    # public Book resources
    books_dao = BooksDAO(db)
    api.add_resource(book_resources.PublicBookList,
                     '/books',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    api.add_resource(book_resources.PublicBook,
                     '/books/<string:book_id>',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    # Authentication resource
    users_dao = UsersDAO(db)
    api.add_resource(auth_resources.Authentication,
                     '/auth',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'users_dao': users_dao
                     })

    return app
