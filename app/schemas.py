from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TweetAdd(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class UserForMe(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserFor(BaseModel):
    user_id: int
    name: str

    class Config:
        orm_mode = True


class UserFull(BaseModel):
    id: int
    name: str
    followers: List[UserForMe] = []
    following: List[UserForMe] = []

    class Config:
        orm_mode = True


class UserMeOut(BaseModel):
    result: bool = True
    user: UserFull

    class Config:
        orm_mode = True


class PictureOut(BaseModel):
    path: str

    class Config:
        orm_mode = True


class TweetsOut(BaseModel):
    id: int
    content: str
    # attachments: List[PictureOut] = []
    attachments: List[str] = []
    author: UserForMe
    likes: List[UserFor]

    class Config:
        orm_mode = True


class TweetResult(BaseModel):
    result: bool = True
    tweets: List[TweetsOut]

    class Config:
        orm_mode = True
