from importlib.resources import contents
from pydoc import ModuleScanner
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
import fastapi
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas  # ,utils
from.database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to database was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(20)

my_post = [{"title": "title of post 1", "content": " content of post 1 ", "id": 1},
           {"title": "title of post 2", "content": " content of post 2 ", "id": 2}]
# @app.get("/")  # decorator+fastapi(app)+http method+path ("/"),("/hgj/jj")
# async def root():
#     return {"message":"Hello World"}


@app.get("/sqlalchemy")
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=List[schemas.Post])
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/post/{id}", response_model=schemas.Post)
def get_single_post(id: int, db: Session = Depends(get_db)):  # response :Response
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id not found : {id}")

    return post


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password  -user.password
    # hashed_password = utils.hash(user.password)
    # user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
