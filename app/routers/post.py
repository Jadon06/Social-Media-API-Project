from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# retrieve social media posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts";""")
    # posts = cursor.fetchall() 
    
    posts = db.query(models.Post).all()
    return posts

# create social media posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO "Posts" ("title", "content", "published") VALUES (%s, %s, %s) RETURNING *;""",(
    #                post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# retrieve a single post
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE "id" = %s;""",(str(id),))
    # post = cursor.fetchall()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post Not Found!!")
    return post

# update a post
@router.put("/{id}")
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE "Posts" SET "title" = %s, "content" = %s , published = %s WHERE "id" = %s RETURNING *;""", 
    #                (post.title, post.content, post.published, str(id),))
    # update_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    return "Post Updated!!"

# delete a post
@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM "Posts" WHERE "id" = %s RETURNING *""", (str(id),))
    # post = cursor.fetchall()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Does Not Exist!")
    
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)