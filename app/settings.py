from environs import Env

env = Env()
env.read_env(".env")

ALGORITHM = "HS256"

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

DATA_BASE_URL = env.str("DATA_BASE_URL")


SQLALCHEMY_DATABASE_URL = DATA_BASE_URL
# SQLALCHEMY_DATABASE_URL = 'sqlite:///db.db'
