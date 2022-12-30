from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, relation
from sqlalchemy.sql import func
from db.database import Base

# alembic init alembic
# alembic revision -m "message"
# alembic revision --message="migrate" --autogenerate
# alembic upgrade head


Followers = Table(
    "followers",
    Base.metadata,
    Column("user", Integer, ForeignKey("users.id")),
    Column("follower", Integer, ForeignKey("users.id")),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

TweetLikeUser = Table(
    "tweet_like",
    Base.metadata,
    Column("tweet", Integer, ForeignKey("tweets.id")),
    Column("user", Integer, ForeignKey("users.id")),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

PostPictures = Table(
    "post_pictures",
    Base.metadata,
    Column("tweet", Integer, ForeignKey("tweets.id")),
    Column("pick", Integer, ForeignKey("pictures.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=False)
    api_key = Column(String, unique=True)
    tweets = relationship("Tweet", back_populates="author", cascade="delete-orphan, all")
    followers = relation(
        "User",
        secondary=Followers,
        primaryjoin=Followers.c.follower == id,
        secondaryjoin=Followers.c.user == id,
        backref="following",
    )
    tweets_like = relationship("Tweet", secondary=TweetLikeUser, back_populates="likes")

    def __str__(self):
        return f"{self.name}"

    def to_dict(self):
        return {
            "result": True,
            "user": {
                "id": self.id,
                "name": self.name,
                "followers": [
                    {"id": user.id, "name": user.name} for user in self.followers
                ],
                "following": [
                    {"id": user.id, "name": user.name} for user in self.following
                ],
            },
        }


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="tweets")
    attachments = relationship(
        "Picture", secondary=PostPictures, back_populates="tweet", cascade="delete, all"
    )
    likes = relationship("User", secondary=TweetLikeUser, back_populates="tweets_like")

    def __str__(self):
        return f"{self.content}"

    def get_list_path(self):
        path_list = []
        [path_list.append(pick.path) for pick in self.attachments]
        return path_list


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
    tweet = relationship("Tweet", secondary=PostPictures, back_populates="attachments")

    def __str__(self):
        return f"{self.path}"
