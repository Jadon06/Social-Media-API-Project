from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# retrieve all social media posts
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, 
              Skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM "Posts";""")
    # posts = cursor.fetchall() 
    posts = db.query(models.Post).filter(models.Post.User_id == current_user.id).filter(models.Post.title.contains(search)).offset(Skip).limit(Limit).all()
    
    # By default SQLAlchemy joins are inner, so isouter=True must be added to specify join type
    results = db.query(models.Post, func.count(
        models.Vote.upvote).label("upvotes"), func.count(models.Vote.downvote).label("downvotes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.User_id == current_user.id).filter(models.Post.title.contains(search)).offset(Skip).limit(Limit).all()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return results

# create social media posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO "Posts" ("title", "content", "published") VALUES (%s, %s, %s) RETURNING *;""",(
    #                post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # conn.commit()
    new_post = models.Post(User_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# retrieve a single post
@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE "id" = %s;""",(str(id),))
    # post = cursor.fetchall()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post, func.count(
        models.Vote.upvote).label("upvotes"), func.count(models.Vote.downvote).label("downvotes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.User_id == current_user.id).filter(models.Post.id == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post Not Found!!")
    # REMINDER - Create a functional security check to ensure current user is accessing their own posts
    # if models.Post.User_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    return results

# update a post
@router.put("/{id}")
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE "Posts" SET "title" = %s, "content" = %s , published = %s WHERE "id" = %s RETURNING *;""", 
    #                (post.title, post.content, post.published, str(id),))
    # update_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.User_id == current_user.id).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    if models.Post.User_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).update(post.dict(), synchronize_session=False)
    db.commit()
    return "Post Updated!!"

# delete a post
@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM "Posts" WHERE "id" = %s RETURNING *""", (str(id),))
    # post = cursor.fetchall()
    # conn.commit()
    print(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Does Not Exist!")
    if current_user.id != post.User_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Post does not belong to you")
    
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)