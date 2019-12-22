from . import abstract_dao


class BooksMemoryDAO(abstract_dao.AbstractBooksDAO):
    """
    Implements the in Memory data access object for the Books
    """
    def __init__(self, db):
        """
        Set the db reference
        """
        self._db = db

    def create_book(self, book_data):
        """"""
        book_data['id'] = len(self._db['books'])
        self._db['books'].append(book_data)
        return self._db['books'][-1]

    def get_all_books(self):
        """
        Returns all books from the database
        """
        return self._db['books']

    def find_book_by_id(self, book_id):
        """
        Get a book by id
        """
        return self._db['books'][int(book_id)]

    def find_book_by_title(self, book_title):
        """
        Get a book by id
        """
        for book in self._db['books']:
            if book['title'] == book_title:
                return book
        return None

    def find_books_by_publisher(self, publisher_id):
        books = []
        for book in self._db['books']:
            if book['publisher'] == publisher_id:
                books.append(book)
        return books

    def delete_book_by_id(self, book_id):
        """
        Delete a book by id
        """
        del self._db['books'][int(book_id)]
        return None
