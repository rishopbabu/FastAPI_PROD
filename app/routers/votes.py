from fastapi import Depends, status, HTTPException, APIRouter # to use fast api
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database # to use fast api methods import other methods
from typing import List

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, 
         db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The vote {vote.post_id} dosen't exists")
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    
    found_vote = vote_query.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted to the post"}
        
    else:
         if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Vote dosen't exist")
        
         vote_query.delete(synchronize_session=False)
         db.commit()
        
         return {"message": "Successfully deleted vote"}