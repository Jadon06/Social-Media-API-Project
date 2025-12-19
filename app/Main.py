from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from random import randrange

app = FastAPI()

conn = psycopg2.connect(host='localhost', database='Social Media API Project Database', 
                        user='postgres', password='mommywoody5623', cursor_factory=RealDictCursor)
cursor = conn.cursor()

class Post(BaseModel):
    title : str
    content : str
    published : bool = False
    liked : Optional[bool] = None

my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, 
            {"title" : "title of post 2", "content" : "content of post 2", "id" : 2}]

# find a post
def find_post(id):
    for post in my_posts:
        if id == post["id"]:
            return post

# find post index
def find_post_index(id):
    for i in range(len(my_posts)):
        if my_posts[i]["id"] == id:
            return i

# retrieve social media posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM "Users";""")
    posts = cursor.fetchall()
    return {"Data" : posts}

# create social media posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO "Users" ("title", "content", "published") VALUES (%s, %s, %s) RETURNING *;""",(
                   post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"Post" : new_post}

# retrieve a single post
@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM "Users" WHERE "id" = %s;""",(str(id),))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post Not Found!!")
    return {"Post" : post}

# update a post
@app.put("/posts/{id}")
def update_post(id : int, post : Post):
    cursor.execute("""UPDATE "Users" SET "title" = %s, "content" = %s , published = %s WHERE "id" = %s RETURNING *;""", 
                   (post.title, post.content, post.published, str(id),))
    update_post = cursor.fetchone()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.commit()
    return {"data" : "post updated!!"} 

# delete a post
@app.delete("/posts/{id}")
def delete_post(id : int):
    cursor.execute("""DELETE FROM "Users" WHERE "id" = %s RETURNING *""", (str(id),))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Does Not Exist!")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)