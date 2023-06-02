from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas , database , models, oauth2 

router=APIRouter(prefix='/votes',tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(database.get_db),
         current_user=Depends(oauth2.get_current_user)):
    
    checking_exsistance=db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if not checking_exsistance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post on whch you are trying to vote does not exsist')

    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                     models.Vote.user_id == current_user.id)
    current_vote=vote_query.first()
    if vote.vote_type==1:
        if current_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with id:{current_user.id} has already casted a vote on post_id:{vote.post_id}')
        create_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(create_vote)
        db.commit()
        
        return {"message":"Your vote has been added successfully"}
    else :
        if not current_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'no xisting vote found for the user')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"} 