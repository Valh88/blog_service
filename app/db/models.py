from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String(10))
    last_name = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=False)
    api_key = Column(String, unique=True)
    tweets = relationship('Tweet', back_populates='user', cascade='delete, all')


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tweets')
    pictures = relationship('Picture', back_populates='tweet', cascade='delete')


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=False)
    tweet = relationship('Tweet', back_populates='pictures')
