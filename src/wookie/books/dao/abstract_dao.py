from abc import ABCMeta, abstractmethod


class AbstractBooksDAO(metaclass=ABCMeta):
    """
    Defines the interface for the Book data access objects
    """
    @abstractmethod
    def create_book(self, book_data):
        raise NotImplementedError

    @abstractmethod
    def get_all_books(self):
        raise NotImplementedError

    @abstractmethod
    def find_book_by_id(self, book_id):
        raise NotImplementedError

    @abstractmethod
    def find_book_by_title(self, book_title):
        raise NotImplementedError

    @abstractmethod
    def find_books_by_publisher(self, publisher_id):
        raise NotImplementedError

    @abstractmethod
    def delete_book_by_id(self, book_id):
        raise NotImplementedError
