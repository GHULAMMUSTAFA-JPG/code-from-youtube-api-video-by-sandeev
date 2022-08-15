from cgitb import text
from enum import unique
from http import server
from tkinter import CASCADE
from sqlalchemy import TIMESTAMP, Column, Integer,String,Boolean, ForeignKey
from sqlalchemy.sql.expression import null,text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship




class Post(Base):
    __tablename__= "posts"
    
    id=Column(Integer,primary_key= True , nullable=False)
    title=Column(String,nullable=False)
    content= Column(String,nullable=False)
    published=Column(Boolean, server_default='True',nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,  ForeignKey("user.id", ondelete="CASCADE") , nullable=False)
    owner= relationship("User")
    
    
    
    
class User(Base):
    __tablename__= "user"
    
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=True)
    phone_number=Column(String)
    


class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),primary_key = True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key = True)