from sqlalchemy import Column,String, Boolean, Integer
from database import Base

#this model represents a database table
class Post(Base):
    __tablename__  = 'post_tb'

    id = Column(Integer, primary_key= True, index= True)
    title = Column(String(100), unique=True, index= True)
    content = Column(String(200))
    published =  Column(Boolean, default= False, index= True)