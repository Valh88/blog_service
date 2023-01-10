from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import settings

if settings.DEBUG:
    DATABASE_URL = "sqlite:///./db.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATA_BASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    data_base = SessionLocal()
    try:
        yield data_base
    finally:
        data_base.close()
