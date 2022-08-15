
from optparse import Option
from sqlalchemy.orm import Session

from app import oauth2
from ..database import SessionLocal, get_db
from .. import models, schemas, utils,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts" ,
    tags=['Posts']
    )






# @router.get("/sqlalchemy")
# def get_posts(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return post


@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),
             limit :int =10 , skip :int=0 , search: Optional[str] =""):
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

        
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post: schemas.PostCreate, db : Session = Depends(get_db), current_user :int=Depends(oauth2.get_current_user)):
    
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # response :Response
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).all()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id not found : {id}")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"NOT authorized to perform requested action")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post=post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")


    if post.owner_id !=current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"NOT authorized to perform requested action")
    
    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"NOT authorized to perform requested action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
