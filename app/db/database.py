from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# alembic revision --message="migrate" --autogenerate
# alembic upgrade head
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    data_base = SessionLocal()
    try:
        yield data_base
    finally:
        data_base.close()
