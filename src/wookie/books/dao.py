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
