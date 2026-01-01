from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # hash the password - user.password
    email_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email of:{user.email}, already exists")
    
    hashed_password = utils.hash(user.password)
    
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get User
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID does not exist")
    return user

# Update User Info
@router.put("/{id}")
def update_user(id: int, user_info: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)    
    db.query(models.User).filter(models.User.id == id).update(user_info.dict())
    db.commit()
    return "Updated Info!!"