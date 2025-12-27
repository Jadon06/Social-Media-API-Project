from jose import JWTError, jwt
from pydantic import EmailStr
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret Key
# Algorithm for encrypting token
# expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acess_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    id: str = payload.get("User_id")
    email: EmailStr = payload.get("email")
    
    if not id or not email:
        raise credentials_exception
    token_data = schemas.TokenData(id=id, email=email)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate" : "Bearere"})
    return verify_access_token(token, credentials_exception)