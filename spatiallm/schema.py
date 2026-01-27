# spatiallm/schema.py
from pydantic import BaseModel
from typing import List


class ArticlePlaces(BaseModel):
    country: str
    city: str
    places: List[str]
