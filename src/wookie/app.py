from flask import Flask
from flask_restful import Api

from . import utils
from .books import resources


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app_logger = utils.create_logger(__name__)

    api.add_resource(resources.Books,
                     '/books',
                     resource_class_kwargs={'logger': app_logger})

    return app
