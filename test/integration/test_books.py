import pytest  # noqa
import json


def test_get_all_books(test_client_with_db):
    """
    Call GET /books
    Get all books from the test db
    """
    url = '/books'
    resp = test_client_with_db.get(url)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)

    assert len(resp.json['data']) == 2
    assert resp.json['data'][0]['id'] == '1'
    assert resp.json['data'][0]['title'] == 'The Wookiee Storybook'
    assert resp.json['data'][0][
        'description'] == 'The Wookiee Storybook description'
    assert resp.json['data'][0]['author'] == 'CB'
    assert resp.json['data'][0]['price'] == 30.0
    assert resp.json['data'][0]['cover'] == 'image-cover-url-1'
    assert 'publisher' not in resp.json['data'][0]
    assert 'links' in resp.json['data'][0]
    assert resp.json['data'][0]['links']['self'] == 'http://localhost/books/1'

    assert resp.json['data'][1]['id'] == '2'
    assert resp.json['data'][1][
        'title'] == 'Wookiee Cookies: A Star Wars Cookbook'
    assert resp.json['data'][1]['author'] == 'CB'
    assert resp.json['data'][1]['price'] == 25.0
    assert resp.json['data'][1]['cover'] == 'image-cover-url-2'
    assert 'publisher' not in resp.json['data'][1]
    assert 'links' in resp.json['data'][1]
    assert resp.json['data'][1]['links']['self'] == 'http://localhost/books/2'


def test_get_public_book_by_id(test_client_with_db):
    """
    GET /book/:id
    Get a public book by id
    """
    url = '/books/1'
    resp = test_client_with_db.get(url)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], dict)
    assert resp.json['data']['id'] == '1'
    assert resp.json['data']['title'] == 'The Wookiee Storybook'
    assert resp.json['data'][
        'description'] == 'The Wookiee Storybook description'
    assert resp.json['data']['author'] == 'CB'
    assert resp.json['data']['price'] == 30.0
    assert resp.json['data']['cover'] == 'image-cover-url-1'
    assert 'publisher' not in resp.json['data']
    assert 'links' in resp.json['data']
    assert resp.json['data']['links']['self'] == 'http://localhost/books/1'


def test_search_non_existing_book_by_title(test_client_with_db):
    """
    GET /books?title=:title
    Search a book that does not exist by title
    """
    url = '/books?title=This book is not in the database'
    resp = test_client_with_db.get(url)
    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'


def test_search_existing_book_by_title(test_client_with_db):
    """
    GET /books?title=:title
    Search a book that exists by title
    """
    url = '/books?title=The Wookiee Storybook'
    resp = test_client_with_db.get(url)
    assert resp.status_code == 200
    assert isinstance(resp.json['data'], dict)
    assert resp.json['data']['id'] == '1'
    assert resp.json['data']['title'] == 'The Wookiee Storybook'
    assert resp.json['data'][
        'description'] == 'The Wookiee Storybook description'
    assert resp.json['data']['author'] == 'CB'
    assert resp.json['data']['price'] == 30.0
    assert resp.json['data']['cover'] == 'image-cover-url-1'
    assert 'publisher' not in resp.json['data']
    assert 'links' in resp.json['data']
    assert resp.json['data']['links']['self'] == 'http://localhost/books/1'


def test_get_all_user_books_for_a_user_with_books(test_client_with_db):
    """
    GET /users/books
    Get all books an authenticated user owns, in this case the user has books
    """
    # first with authenticate the user
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'chewbie', 'password': 'Test1234'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 200
    assert isinstance(resp.json['data'], dict)
    assert 'access_token' in resp.json['data']
    access_token = resp.json['data']['access_token']

    # then get the books the authenticated user owns
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books'

    resp = test_client_with_db.get(url, headers=headers)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)
    assert len(resp.json['data']) == 2
    assert resp.json['data'][0]['id'] == '1'
    assert resp.json['data'][0]['title'] == 'The Wookiee Storybook'
    assert resp.json['data'][0][
        'description'] == 'The Wookiee Storybook description'
    assert resp.json['data'][0]['author'] == 'CB'
    assert resp.json['data'][0]['price'] == 30.0
    assert resp.json['data'][0]['cover'] == 'image-cover-url-1'
    assert 'publisher' not in resp.json['data'][0]
    assert 'links' in resp.json['data'][0]
    assert resp.json['data'][0]['links']['self'] == 'http://localhost/books/1'

    assert resp.json['data'][1]['id'] == '2'
    assert resp.json['data'][1][
        'title'] == 'Wookiee Cookies: A Star Wars Cookbook'
    assert resp.json['data'][1]['author'] == 'CB'
    assert resp.json['data'][1]['price'] == 25.0
    assert resp.json['data'][1]['cover'] == 'image-cover-url-2'
    assert 'publisher' not in resp.json['data'][1]
    assert 'links' in resp.json['data'][1]
    assert resp.json['data'][1]['links']['self'] == 'http://localhost/books/2'


def test_get_all_user_books_for_a_user_without_books(test_client_with_db):
    """
    GET /users/books
    Get all books an authenticated user owns, in this case the user has no
    books
    """
    # first with authenticate the user
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'obi-wan', 'password': 'Test1234'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 200
    assert isinstance(resp.json['data'], dict)
    assert 'access_token' in resp.json['data']
    access_token = resp.json['data']['access_token']

    # then get the books the authenticated user owns
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books'

    resp = test_client_with_db.get(url, headers=headers)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)
    assert len(resp.json['data']) == 0
