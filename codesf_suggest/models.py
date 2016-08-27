import os.path

from flask.json import jsonify

from flask import url_for
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Sequence, ForeignKey, Enum, 
from sqlalchemy.orm import relationship, validates, column_property, backref


from .database import Base, engine

class User(Base):
    """ Base User Class """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    organization = Column(Text)
    position = Column(Text)
    description = Column(Text)
    start_date = Column(DateTime)

    # Foreign relationships
    posts = relationship("Post", backref="admin", cascade="all, delete-orphan")
    volunteered_posts = relationship("Post", backref="user")


class Post(Base):
    """ Base Post Class """
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    short_description = Column(Text)
    long_description = Column(Text)
    organization = Column(Text)
    image = Column(Text)

    # Foreign relationships
    admin_id = Column(Integer, ForeignKey("User.id"))



