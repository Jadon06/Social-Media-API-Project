from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import update
from .. import schemas, models, oauth2

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post of {vote.post_id} does not exist!")
   
    voted = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.voter_id == current_user.id).first()
    
    
    if vote.choice == "unvote" and voted:
        db.query(models.Vote).filter(models.Vote.post_id == vote.post_id and models.Vote.voter_id == current_user.id).delete()
        raise HTTPException(status.HTTP_200_OK, detail="Vote was removed successfully!!")
    
    
    if not voted:
        if vote.choice == 'upvote':
            like = models.Vote(post_id=vote.post_id, voter_id=current_user.id, upvote=True)
            db.add(like)
            db.commit()
        if vote.choice == 'downvote':
            dislike = models.Vote(post_id=vote.post_id, voter_id=current_user.id, downvote=True)
            db.add(dislike)
            db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    # REMINDER - Fix logic for allowing only one unique vote at a time(Cannot allow user to upvote and downvote at the same time)
    # if (voted.upvote and vote.choice == 'upvote') or (voted.downvote and vote.choice == 'downvote'):
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
    #                         detail=f"User {current_user.id} has already voted on post {vote.post_id}! Must change vote choice")
    # if voted:
    #     if vote.choice == 'upvote' and not voted.upvote:
    #         updated_like = (update(models.Vote).where(models.Vote.post_id 
    #                                                 == vote.post_id).where(
    #                                                     models.Vote.voter_id == current_user.id).values(
    #                     {
    #                         models.Vote.upvote: True,
    #                         models.Vote.downvote: None
    #                     }
    #                 )
    #             )
    #         db.execute(updated_like)
    #         db.commit()
    #     if vote.choice == 'downvote' and not voted.downvote:
    #         updated_dislike = (update(models.Vote).where(models.Vote.post_id 
    #                                                 == vote.post_id).where(
    #                                                     models.Vote.voter_id == current_user.id).values(
    #                     {
    #                         models.Vote.downvote: True,
    #                         models.Vote.upvote: None
    #                     }
    #                 )
    #             )
    #         db.execute(updated_dislike)
    #         db.commit()
    return "Vote has been placed Successfully!"