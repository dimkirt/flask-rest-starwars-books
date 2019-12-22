import pytest  # noqa

import wookie.app as app


@pytest.fixture
def test_client():
    test_app = app.create_app()
    return test_app.test_client()
