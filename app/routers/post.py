from ..import models,schemas,oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional

router=APIRouter(prefix='/posts',tags=['Posts'])

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0,search:Optional[str]=""):
    
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    posts=db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # new_post=models.Post(title=post.title,content=post.content,
    #             published=post.published,id=3)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    if post.Post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User not authorized to perform requestd action')
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'posts with id:{id} does not exits')
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User not authorized to perform requestd action')
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post_details:schemas.PostCreate,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post wiht id:{id} does not exits')
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User not authorized to perform requestd action')
    # post_query.update({'title':'ksdlafo','content':'dkas slkadf  askldfjkl jklk'},synchronize_session=False)
    post_query.update(post_details.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()



