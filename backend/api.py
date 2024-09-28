from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv

from buildings import get_buildings
# from ical import GetLecturesInBuilding
from ical import GetLecturesInBuilding, GetTodaysBuildings, ImportCalanderFromLink
from models import Building, Event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class thing(BaseModel):
    calendar: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/calendarlink")
def post_calendar(url: thing):
    ImportCalanderFromLink(url.calendar)
    return True

@app.get("/buildings")
def read_buildings() -> dict[str, Building]:
    return get_buildings()

@app.get("/timetable/building/{building_number}")
def read_timetable_building(building_number: str) -> list[Event]:
    lectures = GetLecturesInBuilding(building_number)
    buildings = get_buildings()

    events = []
    for event in lectures:
        building = buildings[building_number]
        currentlocation = event.location.split(" ")
        room = currentlocation[2]
        events.append(Event(name=event.name, building=building_number, room=room, begin=event.begin.timestamp(), end=event.end.timestamp(), longitude=building.longitude, latitude=building.latitude))

    return events

@app.get("/todaybuildings")
def read_todays_buildings() -> list[Building]:
    return GetTodaysBuildings()
