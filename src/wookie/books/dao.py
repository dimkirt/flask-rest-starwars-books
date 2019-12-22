class BooksDAO(object):
    """"""
    def __init__(self, db):
        """
        Set the db reference
        """
        self._db = db

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
