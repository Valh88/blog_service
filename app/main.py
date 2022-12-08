from fastapi import FastAPI
from routers import tweets
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tweets.router)


@app.get('/')
async def test():
    return '123'
