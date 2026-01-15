from app import schemas, oauth2
from app.routers import auth
from fastapi import status, HTTPException
import pytest

# must pass in client to make HTTP requests

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

@pytest.mark.parametrize("email, password, status_code", [('wrongemail@gmail.com', 'password123', 403),
                                                          ('aycjadon@gmail.com', 'wrongpassword', 403),
                                                          ('wrongemail@gmail.com', 'wrongpassword', 403),
                                                          (None, 'password123', 403),
                                                          ('aycjadon@gmail.com', None, 403)
                                                          ])
def test_failed_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={'username': email, 'password':password})
    assert res.status_code == status_code
    assert res.json().get('detail') == "Invalid email or password!"


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert schemas.UserResponse(**res.json()) == schemas.UserResponse(**test_user)