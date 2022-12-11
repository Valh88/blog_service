from fastapi import FastAPI
from routers import tweets, users
from fastapi import Depends
from db import models
from db.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)


from db.database import get_db
from db.models import User, Picture, Tweet
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# templates = Jinja2Templates(directory="static")


@app.get('/')
async def test(db=Depends(get_db)):

    return 'ok'


# @app.get("/index", response_class=HTMLResponse)
# async def read_all_by_user(request: Request):
#
#
#     return templates.TemplateResponse("index.html", {"request": request})
