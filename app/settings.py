from environs import Env
from loguru import logger
import sys

env = Env()
env.read_env()

ALGORITHM = "HS256"

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

DATA_BASE_URL = env.str("DATA_BASE_URL")

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)
logger.add("./log.log", rotation="5 MB")
