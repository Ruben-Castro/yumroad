import pytest
from flask import url_for
from yumroad import create_app
from yumroad.extensions import db
from yumroad.models import User



@pytest.fixture
def app():
    return create_app('test')

@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture
def authenticated_request(client):
    new_user = User.create('test@example.com', "examplepass")
    db.session.add(new_user)
    db.session.commit()


    response = client.post(url_for('user.login'), data={
        'email': "test@example.com",
        'password': 'examplepass'
    }, follow_redirects=True)

    yield client