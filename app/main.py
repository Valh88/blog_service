from fastapi import FastAPI
from routers import tweets, users, media

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(media.router)


@app.get('/')
async def test():

    return 'ok'
