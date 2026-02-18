# spatiallm/schema.py
from pydantic import BaseModel
from typing import List


class ArticlePlaces(BaseModel):
    country: str
    city: str
    places: List[str]

class Place(BaseModel):
    name: str
    type: str
    desc: str