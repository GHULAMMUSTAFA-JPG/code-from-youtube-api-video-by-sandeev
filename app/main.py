# from passlib.context import CryptContext

# from fastapi import FastAPI ,Response , status,HTTPException, Depends
from fastapi import FastAPI
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
from .import models #, schemas, utils
from.database import engine, SessionLocal, get_db
# from passlib.context import CryptContext
from .routers import post, users, auth ,vote
from .config import settings



#pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app= FastAPI()


    
my_post = [{"title": "title of post 1", "content" : " content of post 1 ", "id" : 1 }   ,
            {"title" : "title of post 2", "content" : " content of post 2 ", "id" : 2  }]


app.include_router(post.router)
app.include_router(users.router)    
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")  # decorator+fastapi(app)+http method+path ("/"),("/hgj/jj")
async def root():
    return {"message": "Hello World"}
