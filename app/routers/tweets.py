import shutil
import uuid
from typing import List
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
    return {"result": True, "tweets": [schemas.TweetsOut.from_orm(tweet) for tweet in tweets]}


@router.post('/tweets', response_model=schemas.TweetSchema)
async def create_tweet(tweet: schemas.TweetSchema):
    pass
    return tweet


@router.post('/medias')
async def get_upload_picture(picture: UploadFile = File(...)):
    picture.filename = str(uuid.uuid4()) + '.jpg'
    path = f"media/{picture.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(picture.file, buffer)

    return JSONResponse({"result": True})


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