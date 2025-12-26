# imports
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session 

from random import randrange
from typing import List

from .routers import post, user

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

app.include_router(post.router)
app.include_router(user.router)