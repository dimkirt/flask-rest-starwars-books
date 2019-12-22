from flask_restful import Resource


class BaseResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs['logger']


class Books(BaseResource):
    """
    Resource for all the books
    """
    def get(self):
        """
        Return a JSON array of all books
        """
        self.logger.info('GET /books')
        books = [{'title': 'Paok'}]
        return {'count': len(books), 'items': books}, 200
