import pytest  # noqa


def test_get_all_books(test_client):
    """
    Get all books from the test db
    """
    url = '/books'
    resp = test_client.get(url)

    assert resp.status_code == 200
    assert isinstance(resp.json['data'], list)

    assert resp.json['data'][0]['title'] == 'This is the title'
