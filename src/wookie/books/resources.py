from flask_restful import Resource


class BaseResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs['logger']
        self.dao = kwargs['dao']


class Books(BaseResource):
    """
    Resource for all the books
    """
    def get(self):
        """
        Return a JSON array of all books
        """
        self.logger.info('GET /books')
        books = self.dao.get_all_books()
        return {'count': len(books), 'items': books}, 200
