# imports
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session 

from typing import Optional
from random import randrange

# creates all database tables defined within the models file
models.Base.metadata.create_all(bind=engine)

# app module for calling fastapi
app = FastAPI()

# connection module for linking postgres database with python program
conn = psycopg2.connect(host='localhost', database='Social Media API Project Database', 
                        user='postgres', password='mommywoody5623', cursor_factory=RealDictCursor)
# cursor module for executing sql methods
cursor = conn.cursor()

# Post model for validation
class Post(BaseModel):
    title : str
    content : str
    published : Optional[bool] = False
    liked : Optional[bool] = None

# NOTE - must pass in 'db: Session = Depends(get_db)' into the function argument to access table

# test query
@app.get("/sqlalchemy")
# Calling the Session function as an object and passing in the function 'get_db' as a argument of 'Depends' to make it a dependency
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Posts" : posts}


# retrieve social media posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts";""")
    # posts = cursor.fetchall() 
    
    posts = db.query(models.Post).all()
    return {"Data" : posts}

# create social media posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO "Posts" ("title", "content", "published") VALUES (%s, %s, %s) RETURNING *;""",(
    #                post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Post" : new_post}

# retrieve a single post
@app.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE "id" = %s;""",(str(id),))
    # post = cursor.fetchall()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post Not Found!!")

    return {"Post" : post}

# update a post
@app.put("/posts/{id}")
def update_post(id : int, post : Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE "Posts" SET "title" = %s, "content" = %s , published = %s WHERE "id" = %s RETURNING *;""", 
    #                (post.title, post.content, post.published, str(id),))
    # update_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data" : "post updated!!"} 

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