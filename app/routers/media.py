from pathlib import Path
import uuid
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse
from db.database import get_db
from db import models
from sqlalchemy.orm import Session
import aiofiles
from settings import logger

router = APIRouter(prefix="/api", tags=["media"])


@router.post("/medias")
@logger.catch
async def get_upload_picture(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    filename = str(uuid.uuid4()) + ".jpg"
    path = str(Path(__file__).parents[2]) + "/images" + f"/{filename}"
    async with aiofiles.open(path, "w+b") as buffer:
        file = await file.read()
        await buffer.write(file)
    url = f"/api/media/{filename}"
    pick = models.Picture(path=url)
    db.add(pick), db.commit()
    return {"result": True, "media_id": pick.id}


@router.get("/media/{name}", response_class=FileResponse)
@logger.catch
def get_file(name: str):
    return f"api/media/{name}"
