from pathlib import Path
import shutil
import uuid
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from db.database import get_db
from db import models
from sqlalchemy.orm import Session
from settings import URL

router = APIRouter(prefix="/api", tags=["media"])


@router.post("/medias")
async def get_upload_picture(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    file.filename = str(uuid.uuid4()) + ".jpg"
    path = str(Path(__file__).parents[2]) + "/images" + f"/{file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = URL + f"/api/media/{file.filename}"
    # __________________________________________________________________
    pick = models.Picture(path=url, tweet_id=1)
    db.add(pick)
    db.commit()
    return {"result": True, "media_id": pick.id}


@router.get("/media/{name}", response_class=FileResponse)
def get_file(name: str):
    pass
