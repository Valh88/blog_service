import shutil
import uuid
from typing import List, Dict
from fastapi import APIRouter, File, Form, UploadFile, Depends
import schemas
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from security import get_apikey_header

router = APIRouter(
  prefix='/api',
  tags=['tweets']
)


@router.get('/tweets', response_model=schemas.TweetResult)
async def all_tweets(api_key: str = Depends(get_apikey_header),
                     db: Session = Depends(get_db)) -> schemas.TweetResult:
    tweets = db.query(models.Tweet).all()
    return {"result": True, "tweets": [schemas.TweetsOut(id=tweet.id,
                                                         content=tweet.id,
                                                         author=tweet.author,
                                                         likes=tweet.likes,
                                                         attachments=tweet.get_list_path()) for tweet in tweets]}


@router.post('/tweets')
async def create_tweet(tweet: schemas.TweetAdd, api_key: str = Depends(get_apikey_header),
                       db: Session = Depends(get_db)):
    print(tweet.tweet_data, tweet.tweet_media_ids)

    return {"result": True, "tweet_id": 1}


@router.delete('/tweets/{id:int}')
async def delete_tweet(id: int):


    return JSONResponse({"result": True})


@router.post('/tweets/{id:int}/likes')
async def like_tweet(id: int):


    return JSONResponse({"result": True})


@router.post('/tweets/{id:int}/follow')
async def follow_to_user(id):


    return JSONResponse({"result": True})


@router.delete('/tweets/{id:int}/follow')
async def delete_follow_to_user(id):

    return JSONResponse({"result": True})
