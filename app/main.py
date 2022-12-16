from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import tweets, users, media

app = FastAPI()

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(media.router)

origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080/",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

