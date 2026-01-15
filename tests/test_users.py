from .database import client, session
from app import schemas, oauth2
from fastapi import status, HTTPException
import pytest

# must pass in client to make HTTP requests

@pytest.fixture(scope='function') # limit scope to the function so that once function has executed the data will be dropped. Prevents dependancy
def test_user(client):
    res = client.post("/users/", json={"email": "aycjadon@gmail.com", "password": "password123"}) # creates a request to create a user and stores the response
    new_user = res.json() # grab that response and convert it into readable JSON which is also a dict
    new_user['password'] = "password123" # append the password so that it's accessable since in our schemas we prevented the password from being returned to user
    return new_user

def test_create_user(client):
    res = client.post("/users/", json={"email": "aycjadon@gmail.com", "password": "password123"})
    
    new_user = schemas.UserResponse(**res.json()) # Validate that the response follows the 'UserResponse' schema. Will be considered a fail if pydantic throws an error
    assert res.json().get("email") == 'aycjadon@gmail.com' 
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login", data={'username': test_user['email'], 'password':test_user['password']})
    login_res = schemas.Token(**res.json())
    token_data = oauth2.verify_access_token(login_res.access_token, credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)) # call the verify access token function which returns token data in the schemas.TokenData format and stores info in var
    
    assert token_data.email == test_user['email'] and int(token_data.id) == test_user['id'] 
    assert res.status_code == 200

def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert schemas.UserResponse(**res.json()) == schemas.UserResponse(**test_user)