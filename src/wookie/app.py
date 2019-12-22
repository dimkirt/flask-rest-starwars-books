from flask import Flask
from flask_restful import Api

from .books import resources


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(resources.Books, '/books')
    return app
