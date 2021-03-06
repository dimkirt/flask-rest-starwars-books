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


def test_unpublish_book_user_owns(test_client_with_db):
    """
    DELETE /users/books/:id
    Unpublish a book that belongs to the authenticated user
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

    # then delete a book this user owns
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books/1'

    resp = test_client_with_db.delete(url, headers=headers)

    assert resp.status_code == 204
    # finally get the books the authenticated user owns
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books'

    resp = test_client_with_db.get(url, headers=headers)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)
    assert len(resp.json['data']) == 1

    assert resp.json['data'][0]['id'] == '2'
    assert resp.json['data'][0][
        'title'] == 'Wookiee Cookies: A Star Wars Cookbook'
    assert resp.json['data'][0]['author'] == 'CB'
    assert resp.json['data'][0]['price'] == 25.0
    assert resp.json['data'][0]['cover'] == 'image-cover-url-2'
    assert 'publisher' not in resp.json['data'][0]
    assert 'links' in resp.json['data'][0]
    assert resp.json['data'][0]['links']['self'] == 'http://localhost/books/2'


def test_unpublish_book_user_does_not_own(test_client_with_db):
    """
    DELETE /users/books/:id
    Try to unpublish a book that does not belong to the authenticated user
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

    # then try delete a book that does not belong to the user
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books/2'

    resp = test_client_with_db.delete(url, headers=headers)
    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'


def test_unpublish_books_that_does_not_exist(test_client_with_db):
    """
    DELETE /users/books/:id
    Try to unpublish a book that does not exist
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

    # then try delete a book that does not exist
    headers = {'Authorization': 'Bearer ' + access_token}
    url = '/users/books/3'

    resp = test_client_with_db.delete(url, headers=headers)

    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'


def test_publish_book(test_client_with_db):
    """
    POST /users/books
    An authenticated user publish a new book
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

    # then try post a new book
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + access_token
    }

    data = {
        'title':
        'How to Speak Wookiee: A Manual for Intergalactic Communication',
        'description': 'This is the description',
        'price': 12.0,
        'cover': 'image-cover-url-3'
    }
    url = '/users/books'

    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.status_code == 201
    assert isinstance(resp.json['data'], dict)
    assert resp.json['data']['id'] == '3'
    assert resp.json['data']['title'] == \
        'How to Speak Wookiee: A Manual for Intergalactic Communication'
    assert resp.json['data']['description'] == 'This is the description'
    assert resp.json['data']['author'] == 'CB'
    assert resp.json['data']['price'] == 12.0
    assert resp.json['data']['cover'] == 'image-cover-url-3'
    assert 'publisher' not in resp.json['data']
    assert 'links' in resp.json['data']
    assert resp.json['data']['links']['self'] == 'http://localhost/books/3'


def test_publish_book_with_existing_title(test_client_with_db):
    """
    POST /users/books
    An authenticated user tries to publish a new book but with an
    existing title
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

    # then try post a new book
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + access_token
    }

    data = {
        'title': 'The Wookiee Storybook',
        'description': 'This is the description',
        'price': 12.0,
        'cover': 'image-cover-url-3'
    }
    url = '/users/books'

    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)
    assert resp.status_code == 400
    assert resp.json['message'] ==\
        'The browser (or proxy) sent a request that this server'\
        ' could not understand.'


def test_publish_book_as_darth_vader(test_client_with_db):
    """
    POST /users/books
    The user with the author_pseudonym `_Darth Vader_` is explicitly black
    listed
    """
    # first with authenticate the user
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'lord-vader', 'password': 'letmein'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 200
    assert isinstance(resp.json['data'], dict)
    assert 'access_token' in resp.json['data']
    access_token = resp.json['data']['access_token']

    # then try post a new book
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + access_token
    }

    data = {
        'title': 'The Wookiee Storybook',
        'description': 'This is the description',
        'price': 12.0,
        'cover': 'image-cover-url-3'
    }
    url = '/users/books'

    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)
    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'
