# imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from . import models
from .database import engine

from .routers import post, user, auth, vote

from .config import settings
# creates all database tables defined within the models file
# models.Base.metadata.create_all(bind=engine)

# app module for calling fastapi
app = FastAPI()

origins = ["https://www.google.com/"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# NOTE - must pass in 'db: Session = Depends(get_db)' into the function argument to access table

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# check that API is running
@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}
