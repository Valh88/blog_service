from fastapi import APIRouter, Depends, HTTPException, status
import schemas
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from security import get_apikey_header, get_current_user

router = APIRouter(
  prefix='/api',
  tags=['tweets']
)


@router.get('/tweets', response_model=schemas.TweetResult)
async def all_tweets(current_user: schemas.UserFull = Depends(get_current_user),
                     db: Session = Depends(get_db)) -> schemas.TweetResult:
    tweets = db.query(models.Tweet).all()
    return {"result": True, "tweets": [schemas.TweetsOut(id=tweet.id,
                                                         content=tweet.id,
                                                         author=tweet.author,
                                                         likes=tweet.likes,
                                                         attachments=tweet.get_list_path()) for tweet in tweets]}


@router.post('/tweets')
async def create_tweet(tweet: schemas.TweetAdd, current_user: schemas.UserFull = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    tweet = models.Tweet(content=tweet.tweet_data, author_id=current_user.id)
    db.add(tweet), db.commit()
    return {"result": True, "tweet_id": tweet.id}


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
