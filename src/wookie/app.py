from flask import Flask
from flask_restful import Api

import flask_jwt_extended

from . import utils
from .books.dao.memory_dao import BooksMemoryDAO
from .users.dao.memory_dao import UsersMemoryDAO

from .books import resources as book_resources
from .users import resources as user_resources


def create_app(db):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # TODO: Move this to env var

    api = Api(app)
    flask_jwt_extended.JWTManager(app)

    app_logger = utils.create_logger(__name__)

    books_dao = BooksMemoryDAO(db)
    users_dao = UsersMemoryDAO(db)

    # public Book resources
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

    # Books resources owned by Users
    api.add_resource(book_resources.UserBookList,
                     '/users/books',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    api.add_resource(book_resources.UserBook,
                     '/users/books/<string:book_id>',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    # Authentication resource
    api.add_resource(user_resources.UserAuthentication,
                     '/auth',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'users_dao': users_dao
                     })

    return app
