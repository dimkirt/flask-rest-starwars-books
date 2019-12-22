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


class Book(BaseResource):
    """
    Resource for one book
    """
    def get(self, book_id):
        """
        Get a book by id
        """
        self.logger.info('GET /books/${}'.format(book_id))

        book = self.dao.find_book_by_id(book_id)
        return book, 200
