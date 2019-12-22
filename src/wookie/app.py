from flask import Flask
from flask_restful import Api

from . import utils
from .books import resources as book_resources
from .books.dao import BooksDAO


def create_app():
    app = Flask(__name__)
    api = Api(app)

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
        }]
    }

    books_dao = BooksDAO(db)
    api.add_resource(book_resources.Books,
                     '/books',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    api.add_resource(book_resources.Book,
                     '/books/<string:book_id>',
                     resource_class_kwargs={
                         'logger': app_logger,
                         'books_dao': books_dao
                     })

    return app
