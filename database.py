from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql://postgres:clumsy23@localhost:5432/Posts'

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()