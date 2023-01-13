from tests.conftest import client, create_data
from db.models import User, Tweet


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


def test_endpoint(db):
    create_data(db)
    response = client.get("api/users/me")
    assert response.status_code == 401
    assert response.text == '{"detail":"Invalid user or key"}'

    client.headers = {"api-key": "test2"}

    response = client.get("api/users/me")
    assert response.status_code == 200

    data = response.json()
    assert data["result"]

    response = client.get("api/tweets")
    data = response.json()
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

    with open("./test_image.jpg", mode="rb") as file:
        data = file.read()
    response = client.post(
        "api/medias", files={"file": data}, headers={"api-key": "test2"}
    )
    assert response.status_code == 200
