from fastapi import FastAPI
from pydantic import BaseModel
import csv

from buildings import get_buildings
# from ical import GetLecturesInBuilding
from models import Building

app = FastAPI()





def parse_event(event):
    return 

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/buildings")
def read_buildings() -> dict[str, Building]:
    return get_buildings()

@app.get("/timetable")
def read_timetable(timetable_url: str):
    return "Placeholder"

@app.get("/timetable/building/{building_number}")
def read_timetable_building(building_number: str):
    return GetLecturesInBuilding()

