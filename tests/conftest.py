# All files in the 'tests' package can access the conftest content

from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from app.Main import app
import pytest
from app import schemas, database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

from alembic import command


# URL format - SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# client = TestClient(app) replaced by fixture made below

# def test_root():
#     response = client.get("/")
#     assert response.json().get('message') == 'API is running' and response.status_code == 200

# Changes scope so that the fixture will last the entirety of the module, currently inly 'test_users'

@pytest.fixture(scope="function")
def session():
    # run to remove all data to start on a clean slate
    database.Base.metadata.drop_all(bind=engine)
    # run our code before we return our test to make all tables
    database.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    # Pass in session so that function depends on session fixture
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # override the chosen dependecy so that we don't make changes to the live databases
    app.dependency_overrides[database.get_db] = override_get_db
    # returns the module TestClient(app)
    yield TestClient(app)

@pytest.fixture(scope='function') # limit scope to the function so that once function has executed the data will be dropped. Prevents dependancy
def test_user(client):
    res = client.post("/users/", json={"email": "aycjadon@gmail.com", "password": "password123"}) # creates a request to create a user and stores the response
    new_user = res.json() # grab that response and convert it into readable JSON which is also a dict
    new_user['password'] = "password123" # append the password so that it's accessable since in our schemas we prevented the password from being returned to user
    return new_user

@pytest.fixture
def test_post(client):
    res = client.post("/posts/", json={'title': 'Awesome Cities in Canada', 'content': 'Toronto, Whistler, Vancouver', 'published': True})
    new_post = res.json()
    return new_post