from pydantic import BaseModel


class Event(BaseModel):
    name: str
    building: str
    room: str
    begin: int
    end: int
    longitude: float
    latitude: float

class Building(BaseModel):
    name: str
    number: str
    longitude: float
    latitude: float

