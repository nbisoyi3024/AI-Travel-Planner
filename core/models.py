#schema

from pydantic import BaseModel
from typing import List

class TravelOutput(BaseModel):
    answer: dict
    places: List[str]
    tips: List[str]
    itineraries: str