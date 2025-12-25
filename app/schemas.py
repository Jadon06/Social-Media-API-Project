# imports
from pydantic import BaseModel
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