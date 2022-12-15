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


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
session = SessionLocal()


def test_models():
    pass

