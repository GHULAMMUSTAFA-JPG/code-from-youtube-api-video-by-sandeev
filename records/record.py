from importlib.resources import contents
from pydoc import ModuleScanner
from typing import Optional
from fastapi import FastAPI ,Response , status,HTTPException, Depends
import fastapi
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from.database import engine,SessionLocal, get_db
models.Base.metadata.create_all(bind=engine)

app= FastAPI()

 


while True:
    try:
        conn= psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Connection to database was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(20)
    
my_post = [{"title": "title of post 1", "content" : " content of post 1 ", "id" : 1 }   ,
            {"title" : "title of post 2", "content" : " content of post 2 ", "id" : 2  }]

@app.get("/")  # decorator+fastapi(app)+http method+path ("/"),("/hgj/jj")
async def root():
    return {"message":"Hello World"}

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    post=db.query(models.Post).all()
    print(post)
    return {"status": post} 



@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    post = db.query(models.Post).all()
    return {"data" : post }

# @app.get("/createposts")
# def create_posts(payloads: dict = Body(...)):
#     print(payloads)
#     return{"new_posts"  :  f"title{payloads['title']} content : {payloads['content']} " }
    # print(post)
    # print(post.dict())  #3convert any pydantic model to dict() using .dict()
    # -----------------------------------------------------
   
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange (0,100000)
    # my_post.append(post_dict)
    
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES( %s , %s , %s ) RETURNING* """,
    #                (post.title, post.content, post.published))
    # pst = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
#  **post.dict() ->same as   --> title=post.title,content=post.content,published=post.published  <--  so for large no of fields use **post.dict() it will even add field to i if more fields are added to the table
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

@app.get("/post/{id}") # id represents the path perameter
def get_post(id: int, db: Session = Depends(get_db)):  # response :Response
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return{"message":f"post with id not found {id}"}
    # print(post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id not found : {id}")

    #post=find_post(int(id))
    # cursor.execute(""" SELECT* FROM posts WHERE id = %s """,(str(id)))
    # post=cursor.fetchone()    
    
    post=db.query(models.Post).filter(models.Post.id == id).first()
    # if you know there could be more than one id use .all() otherwise don't it will use postgresql resources 
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id not found : {id}")
    return {"post_details" : post}

def find_index(id):
    for i, p in enumerate(my_post):
        if p['id']==id:
            return i

@app.delete("/post/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    #index=find_index(id)
    #my_post.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING*  """, (str(id)))
    # delete_post=cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    # if you know there could be more than one id use .all() otherwise don't it will use postgresql resources
    print(post)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/post/{id}") 
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    # print(post)
    # index = find_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id : {id} does not exist")
    # post_dict=post.dict()
    # post_dict["id"] = id
    # my_post[index]=post_dict
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id : {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"message": post_query.first()}
    
    




