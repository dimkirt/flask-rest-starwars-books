from flask_restful import Resource, fields, marshal_with, request, abort


class BaseResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs['logger']
        self.dao = kwargs['dao']


getBookDto = {
    'id': fields.String,
    'title': fields.String,
    'author': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'cover': fields.String,
    'links': {
        'self': fields.FormattedString('{host}books/{id}')
    }
}


class Books(BaseResource):
    """
    Resource for all the books
    """
    @marshal_with(getBookDto, envelope='data')
    def get(self):
        """
        Return a JSON array of all books
        """
        # Search by title
        args = request.args
        if 'title' in args:
            self.logger.info('GET /books?title={}'.format(args['title']))
            book = self.dao.find_book_by_title(args['title'])
            if book is None:
                abort(403)
            book['host'] = request.host_url
            return book, 200

        self.logger.info('GET /books')
        books = self.dao.get_all_books()
        for book in books:
            book['host'] = request.host_url

        return books, 200


class Book(BaseResource):
    """
    Resource for one book
    """
    @marshal_with(getBookDto, envelope='data')
    def get(self, book_id):
        """
        Get a book by id
        """
        self.logger.info('GET /books/${}'.format(book_id))
        book = self.dao.find_book_by_id(book_id)
        book['host'] = request.host_url
        return book, 200
