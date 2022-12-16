import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
from main import app
from db.models import User, Picture, Tweet
from db.database import get_db, sessionmaker, create_engine, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db

    db.rollback()
    connection.close()


@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def create_data(db):
    user1 = User(name="test1", api_key="test1")
    user2 = User(name="test2", api_key="test2")
    user3 = User(name="test3", api_key="test3")

    user2.following.append(user3)
    user2.following.append(user1)
    user1.following.append(user3)

    db.add(user1), db.add(user2), db.add(user3)

    tweet1 = Tweet(content="tweet1", author_id=user2.id)
    tweet2 = Tweet(content="tweet2", author_id=user2.id)
    tweet3 = Tweet(content="tweet3", author_id=user1.id)
    tweet4 = Tweet(content="tweet4", author_id=user3.id)
    tweet1.likes.append(user1)
    tweet3.likes.append(user2)
    tweet4.likes.append(user1)

    db.add(tweet1), db.add(tweet2), db.add(tweet3), db.add(tweet4)

    pick1 = Picture(
        path="http://127.0.0.1:8080/api/media/c2044402-8812-4e35-9d39-75a83b1db1bb.jpg",
        tweet_id=0,
    )
    pick2 = Picture(
        path="http://127.0.0.1:8080/api/media/1cde96d0-6bb1-4fbd-85c5-c99ea60b1d8e.jpg",
        tweet_id=0,
    )

    tweet1.attachments.append(pick1)
    tweet2.attachments.append(pick2)
    db.add(tweet1), db.add(tweet2)
    db.commit()


def test_models(db):
    user = User(name="test1", api_key="test1")
    db.add(user), db.commit()

    user = db.query(User).filter(User.api_key == "test1").first()
    assert user.name == "test1"

    user_2 = User(name="test2", api_key="test2")
    user.followers.append(user_2)
    db.add(user), db.commit()

    user = db.query(User).filter(User.api_key == "test1").first()
    followers = user.followers
    assert user_2 == followers[0]

    user.following.append(user_2)
    assert user.following[0] == user_2

    tweet = Tweet(content="tweet1", author=user)
    tweets = user.tweets
    assert tweets[0].content == "tweet1"
    assert tweet.author == user


def test_create_data(db):
    create_data(db)
    assert True


def test_get_current_user():
    response = client.get("api/users/me")
    assert response.status_code == 401
    assert response.text == '{"detail":"Invalid user or key"}'

    client.headers = {"api-key": "test2"}
    response = client.get("api/users/me")
    assert response.status_code == 200

    data = json.loads(response.text)
    assert data["result"]
