from flask_restful import Resource, fields, marshal_with, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


class BaseResource(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs['logger']
        self.books_dao = kwargs['books_dao']


get_book_dto = {
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


class PublicBookList(BaseResource):
    """
    Resource for all the books
    """
    @marshal_with(get_book_dto, envelope='data')
    def get(self):
        """
        Return a JSON array of all books
        """
        # Search by title
        args = request.args
        if 'title' in args:
            self.logger.info('GET /books?title={}'.format(args['title']))
            book = self.books_dao.find_book_by_title(args['title'])
            if book is None:
                abort(403)
            book['host'] = request.host_url
            return book, 200

        self.logger.info('GET /books')
        books = self.books_dao.get_all_books()
        for book in books:
            book['host'] = request.host_url

        return books, 200


class PublicBook(BaseResource):
    """
    Resource for one book
    """
    @marshal_with(get_book_dto, envelope='data')
    def get(self, book_id):
        """
        Get a book by id
        """
        self.logger.info('GET /books/${}'.format(book_id))
        book = self.books_dao.find_book_by_id(book_id)
        if book is None:
            abort(403)
        book['host'] = request.host_url
        return book, 200


class UserBookList(BaseResource):
    """
    BookList Resource that is owned by a User
    """
    @jwt_required
    @marshal_with(get_book_dto, envelope='data')
    def get(self):
        """
        Get all books published by a User
        """
        current_userid = get_jwt_identity()
        books = self.books_dao.find_books_by_publisher(current_userid)

        for book in books:
            book['host'] = request.host_url

        self.logger.info('GET /users/books')
        return books, 200

    @jwt_required
    @marshal_with(get_book_dto, envelope='data')
    def post(self):
        """
        Publish a new book
        """
        book_data = request.get_json()
        current_userid = get_jwt_identity()
        book_data['publisher'] = current_userid

        published_book = self.books_dao.create_book(book_data)
        published_book['host'] = request.host_url

        self.logger.info('POST /users/books')
        return published_book, 201


class UserBook(BaseResource):
    """
    Book Resource that is owned by a User
    """
    @jwt_required
    def delete(self, book_id):
        """
        Allows a User to unpublish a book
        """
        current_userid = get_jwt_identity()
        book = self.books_dao.find_book_by_id(book_id)
        if book is None or book['publisher'] != current_userid:
            abort(403)

        self.books_dao.delete_book_by_id(book_id)
        self.logger.info('DELETE /users/books/${}'.format(book_id))

        return '', 204
