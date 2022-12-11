import os
from pathlib import Path
import shutil
import uuid
from fastapi import APIRouter, File, Form, UploadFile, Depends
import schemas
from fastapi.responses import JSONResponse

router = APIRouter(
  prefix='/api',
  tags=['media']
)


@router.post('/medias')
async def get_upload_picture(file: UploadFile = Form(...)):
    file.filename = str(uuid.uuid4()) + '.jpg'
    path = str(Path(__file__).parents[2]) + f'/images'
    path = f"{path}/{file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"result": True, "media_id": 1}


