from jose import JWTError, jwt
from pydantic import EmailStr
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret Key
# Algorithm for encrypting token
# expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_acess_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    token_id: str = str(payload.get("User_id"))
    token_email: EmailStr = payload.get("email")

    if not token_id or not token_email:
        raise credentials_exception
    token_data = schemas.TokenData(id=token_id, email=token_email)
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate" : "Bearer"})
    token_info = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_info.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email does not exist")
    return user