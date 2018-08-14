from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
# On import create the database engine base for further use
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()

# Class for the structure of the user table
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    salt = Column(String)
 
    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt

Base.metadata.create_all(engine)