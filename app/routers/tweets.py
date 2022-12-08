import shutil
import uuid
from fastapi import APIRouter, File, Form, UploadFile
from schemas import TweetSchema
from fastapi.responses import JSONResponse

router = APIRouter(
  prefix='/api',
  tags=['tweets']
)


@router.post('/tweets')
async def create_tweet(tweet: TweetSchema):
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
async def follow_to_user(id):

    return JSONResponse({"result": True})