from fastapi.testclient import TestClient
from main import app
from db.models import User, Followers, Picture, Tweet
from db.database import SessionLocal


client = TestClient(app)

session = SessionLocal()


def test_models():
    # user3 = User(name='name3')
    # user = User(name='name2')
    # user2 = User(name='name1')
    # session.add(user)
    # session.add(user2)
    # session.add(user3)
    # session.commit()
    user = session.query(User).filter(User.name == 'name1').first()
    user2 = session.query(User).filter(User.name == 'name2').first()
    user3 = session.query(User).filter(User.name == 'name3').first()
    print(user.followers)
    print(user.id)
    print(user.following)

    # tweet = Tweet(content='content', author=user3)
    # session.add(tweet)
    # session.commit()
    print(user3.tweets)
    print(user3.id)
