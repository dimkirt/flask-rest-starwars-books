import pytest  # noqa


def test_get_all_books(test_client_with_db):
    """
    Get all books from the test db
    """
    url = '/books'
    resp = test_client_with_db.get(url)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)

    assert len(list(resp.json['data'])) == 2
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
