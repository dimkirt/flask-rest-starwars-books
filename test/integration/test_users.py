import pytest  # noqa
import json


def test_authenticate_existing_user(test_client_with_db):
    """
    Call /auth
    Authenticates a user that exists in the db
    """
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


def test_authenticate_existing_user_with_missing_fields(test_client_with_db):
    """
    Call /auth
    Try to authenticate a user that exists in the db without providing
    username or password
    """
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'chewbie'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 400
    assert resp.json['message'] ==\
        'The browser (or proxy) sent a request that this server'\
        ' could not understand.'

    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'password': 'Test1234'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 400
    assert resp.json['message'] ==\
        'The browser (or proxy) sent a request that this server '\
        'could not understand.'


def test_authenticate_non_existing_user(test_client_with_db):
    """
    Call /auth
    Try to authenticate a user that does not exist in the db
    """
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'boubis', 'password': 'Test1234'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.content_type == mimetype
    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'


def test_authenticate_user_with_wrong_credentials(test_client_with_db):
    """
    Call /auth
    Try to authenticate a user that exists in the db but with wrong password
    """
    url = '/auth'
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype}
    data = {'username': 'chewbie', 'password': 'Test1234!!!'}
    resp = test_client_with_db.post(url,
                                    data=json.dumps(data),
                                    headers=headers)

    assert resp.status_code == 403
    assert resp.json['message'] ==\
        'You don\'t have the permission to access the requested resource. '\
        'It is either read-protected or not readable by the server.'
