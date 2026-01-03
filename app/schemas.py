# imports
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union
from datetime import datetime
from enum import Enum

# Post model for validation
class PostBase(BaseModel):
    title : str
    content : str
    published : Optional[bool] = False

class PostCreate(PostBase):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostResponse(PostBase):
    pass
    created_at: datetime
    User_id: int
    user: UserLogin
    # tells pydantic that argument being passed is an ORM model allowing conversion
    class Config:
        orm_mode = True

class PostVote(BaseModel):
    pass
    Post: PostResponse
    upvotes: int
    downvotes: int
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None

# voting schema to only allow an upvote or a downvote not both
class Options(str, Enum):
    upvote = "upvote"
    downvote = "downvote"

class Vote(BaseModel):
    choice: Optional[Options] = None
    post_id: int
