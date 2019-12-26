from flask import Flask
from flask_restful import Api

import flask_jwt_extended

from . import utils

from .books import resources as book_resources
from .users import resources as user_resources


def create_app(config):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .db import db as sqldb
    sqldb.init_app(app)

    from .books.dao.sql_dao import BooksSQLDAO
    from .users.dao.sql_dao import UsersSQLDAO

    api = Api(app)
    flask_jwt_extended.JWTManager(app)

    app_logger = utils.create_logger(__name__)

    books_dao = BooksSQLDAO()
    users_dao = UsersSQLDAO()

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
                         'books_dao': books_dao,
                         'users_dao': users_dao,
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
