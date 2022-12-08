from pydantic import BaseModel
from typing import List, Optional, Dict


class TweetSchema(BaseModel):
    data: str
    media: List[int] = []
