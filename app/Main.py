# imports
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session 

from random import randrange
from typing import List

# creates all database tables defined within the models file
models.Base.metadata.create_all(bind=engine)

# app module for calling fastapi
app = FastAPI()

# connection module for linking postgres database with python program
conn = psycopg2.connect(host='localhost', database='Social Media API Project Database', 
                        user='postgres', password='mommywoody5623', cursor_factory=RealDictCursor)
# cursor module for executing sql methods
cursor = conn.cursor()

# NOTE - must pass in 'db: Session = Depends(get_db)' into the function argument to access table

# # test query
# @app.get("/sqlalchemy")
# # Calling the Session function as an object and passing in the function 'get_db' as a argument of 'Depends' to make it a dependency
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"Posts" : posts}

# retrieve social media posts
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts";""")
    # posts = cursor.fetchall() 
    
    posts = db.query(models.Post).all()
    return posts

# create social media posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
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
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE "id" = %s;""",(str(id),))
    # post = cursor.fetchall()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post Not Found!!")

    return post

# update a post
@app.put("/posts/{id}")
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
@app.delete("/posts/{id}")
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