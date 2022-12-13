from fastapi import FastAPI
from routers import tweets, users, media
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(media.router)


# app.mount('/images', StaticFiles(directory='../images'), name='files')


# @app.get('/')
# async def test():
#
#     return 'ok'
