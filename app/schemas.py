# imports
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Post model for validation
class PostBase(BaseModel):
    title : str
    content : str
    published : Optional[bool] = False
    liked : Optional[bool] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    pass
    created_at: datetime
    # tells pydantic that argument being passed is an ORM model allowing conversion
    class Config:
        orm_mode = True

# User validation model
class User(BaseModel):
    email: EmailStr
    password: str

# User Response Model
class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str