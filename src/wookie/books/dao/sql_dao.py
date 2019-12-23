from . import abstract_dao
from ...db import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    cover = db.Column(db.String(400), unique=False, nullable=False)
    publisher = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BooksSQLDAO(abstract_dao.AbstractBooksDAO):
    """
    Implements the in sql data access object for the Books
    """
    def create_book(self, book_data):
        book = Book(title=book_data['title'],
                    author=book_data['author'],
                    description=book_data['description'],
                    price=book_data['price'],
                    cover=book_data['cover'],
                    publisher=book_data['publisher'])
        db.session.add(book)
        db.session.commit()
        return book.as_dict()

    def get_all_books(self):
        books = Book.query.all()
        books_dict = list(map(lambda book: book.as_dict(), books))
        return books_dict

    def find_book_by_id(self, book_id):
        book = Book.query.get(book_id)
        if book is None:
            return None
        return book.as_dict()

    def find_book_by_title(self, book_title):
        book = Book.query.filter_by(title=book_title).first()
        if book is None:
            return None
        return book.as_dict()

    def find_books_by_publisher(self, publisher_id):
        books = Book.query.filter_by(publisher=publisher_id)
        books_dict = list(map(lambda book: book.as_dict(), books))
        return books_dict

    def delete_book_by_id(self, book_id):
        book = Book.query.get(book_id)
        if book is None:
            return None
        db.session.delete(book)
        db.session.commit()
