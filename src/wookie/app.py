from flask import Flask
from flask_restful import Api

from . import utils
from .books import resources
from .books.dao import BooksDAO


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app_logger = utils.create_logger(__name__)
    # Use in-memory storage for now
    db = {'books': [{'title': 'Paok'}]}

    books_dao = BooksDAO(db)
    api.add_resource(resources.Books,
                     '/books',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'dao': books_dao
                     })

    return app
