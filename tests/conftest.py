import pytest
import os
from app import create_app
from app.extensions import db
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='session')
def app():
    app = create_app(config_name='app.config.TestingConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def auth_headers(app):
    with app.app_context():
        access_token = create_access_token(identity="test_user")
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        return headers
