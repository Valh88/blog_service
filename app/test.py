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


def override_get_db():
    connection = engine.connect()
    # transaction = connection.begin()
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


def create_data(db: Session):
    user1 = User(name="test1", api_key="test1")
    user2 = User(name="test2", api_key="test2")
    user3 = User(name="test3", api_key="test3")

    user2.following.append(user3)
    user2.following.append(user1)
    user1.following.append(user3)

    db.add(user1), db.add(user2), db.add(user3)
    db.commit()

    tweet1 = Tweet(content="tweet1", author_id=user2.id)
    tweet2 = Tweet(content="tweet2", author_id=user2.id)
    tweet3 = Tweet(content="tweet3", author_id=user1.id)
    tweet4 = Tweet(content="tweet4", author_id=user3.id)
    tweet1.likes.append(user1)
    tweet3.likes.append(user2)
    tweet4.likes.append(user1)

    db.add(tweet1), db.add(tweet2), db.add(tweet3), db.add(tweet4)
    db.commit()

    pick1 = Picture(path="api/media/c2044402-8812-4e35-9d39-75a83b1db1bb.jpg")
    pick1.tweet.append(tweet1)
    pick2 = Picture(path="api/media/1cde96d0-6bb1-4fbd-85c5-c99ea60b1d8e.jpg")
    pick2.tweet.append(tweet2)
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


def test_current_user():

    response = client.get("api/users/me")
    assert response.status_code == 401
    assert response.text == '{"detail":"Invalid user or key"}'

    client.headers = {"api-key": "test2"}

    response = client.get("api/users/me")
    assert response.status_code == 200

    data = json.loads(response.text)
    assert data["result"]

    response = client.get("api/tweets")
    data = json.loads(response.text)
    assert len(data["tweets"]) == 4

    response = client.post(
        "api/tweets", json={"tweet_data": "test_data", "tweet_media_ids": [0]}
    )
    assert response.text == '{"result":true,"tweet_id":5}'

    response = client.delete("api/tweets/1")
    assert response.status_code == 200
    assert response.text == '{"result":true}'

    response = client.delete("api/tweet/1", headers={"api-key": "test1"})
    assert response.status_code == 404

    client.headers = {"api-key": "test2"}

    response = client.post("api/tweets/2/likes")
    assert response.status_code == 200
    assert response.json() == {"result": True}

    response = client.delete("api/tweets/2/likes")
    assert response.status_code == 200
    assert response.json() == {"result": True}

    response = client.post("api/users/1/follow")
    assert response.status_code == 200
    assert response.json() == {"result": True}

    response = client.delete("api/tweets/1/follow")
    assert response.status_code == 200
    # assert response.json() == {"result": True}

    with open("../test_image.jpg", mode="rb") as file:
        data = file.read()
    response = client.post(
        "api/medias", files={"file": data}, headers={"api-key": "test2"}
    )
    assert response.status_code == 200
