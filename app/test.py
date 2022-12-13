import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from db.models import User, Followers, Picture, Tweet
from db.database import SessionLocal, get_db, sessionmaker, create_engine, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db

    db.rollback()
    connection.close()


# app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
session = SessionLocal()


def test_models():
    Base.metadata.create_all()
    # user3 = User(name='name3')
    # user = User(name='name2')
    # user2 = User(name='name1')
    # session.add(user)
    # session.add(user2)
    # session.add(user3)
    # session.commit()
    # user = session.query(User).filter(User.name == 'name1').first()
    # user2 = session.query(User).filter(User.name == 'name2').first()
    # user3 = session.query(User).filter(User.name == 'name3').first()
    # print(user.followers)
    # print(user.id)
    # print(user.following)

    # tweet = Tweet(content='content', author=user3)
    # session.add(tweet)
    # session.commit()
    # print(user3.tweets)
    # print(user3.id)
    pass


def test_post():
    # client.headers = {'api-key': 'test'}
    response = client.get('/api/tweets', headers={'api-key': 'test'})
    print(response.headers, 111111111111111111111111111111111)
    assert '{"result":true,"tweets":[{"id":1,' \
           '"content":"content","attachments":[],' \
           '"author":{"id":3,"name":"name3"},"likes":[]}]}' == response.text
