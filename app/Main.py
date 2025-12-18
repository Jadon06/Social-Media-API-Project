from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

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
    return {"Data" : my_posts}

# create social media posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,10000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"Post" : post_dict}

# retrieve a single post
@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    return {"Post" : post}

# update a post
@app.put("/posts/{id}")
def update_post(id : int, post : Post, response : Response):
    post_index = find_post_index(id)

    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {"data" : post_dict} 

# delete a post
@app.delete("/posts/{id}")
def delete_post(id : int):
    post_in_my_posts = False
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            post_in_my_posts = True
        if not post_in_my_posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Post id was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
