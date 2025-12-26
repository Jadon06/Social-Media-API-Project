from passlib.context import CryptContext
# Hashing algortihm for User password security
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(pw: str):
    return pwd_context.hash(pw)

def verify(plain_pw: str, database_pw: str):
    return pwd_context.verify(plain_pw, database_pw)