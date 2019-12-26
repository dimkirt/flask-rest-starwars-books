import pytest  # noqa

from wookie.db import db as sqldb
from wookie.books.dao.sql_dao import Book
from wookie.users.dao.sql_dao import User
from wookie.app import create_app


@pytest.fixture
def test_client_with_db():
    test_app = create_app()

    with test_app.app_context():
        # delete existing db
        sqldb.drop_all()

        # create new db
        sqldb.create_all()
        sqldb.session.commit()

        # create users
        obi_wan = User(username='obi-wan',
                       password='Test1234',
                       author_pseudonym='Ken')
        sqldb.session.add(obi_wan)
        sqldb.session.commit()

        chewbacca = User(username='chewbie',
                         password='Test1234',
                         author_pseudonym='CB')
        sqldb.session.add(chewbacca)
        sqldb.session.commit()

        darth_vader = User(username='lord-vader',
                           password='letmein',
                           author_pseudonym='_Darth Vader_')
        sqldb.session.add(darth_vader)
        sqldb.session.commit()

        # create a book title
        book_1 = Book(title='The Wookiee Storybook',
                      author=chewbacca.author_pseudonym,
                      description='The Wookiee Storybook description',
                      price=30.0,
                      cover='image-cover-url-1',
                      publisher=chewbacca.id)
        sqldb.session.add(book_1)
        sqldb.session.commit()

        book_2 = Book(
            title='Wookiee Cookies: A Star Wars Cookbook',
            author=chewbacca.author_pseudonym,
            description='Wookiee Cookies: A Star Wars Cookbook description',
            price=25.0,
            cover='image-cover-url-2',
            publisher=chewbacca.id)
        sqldb.session.add(book_2)
        sqldb.session.commit()

    return test_app.test_client()
