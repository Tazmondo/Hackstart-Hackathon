# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz

from buildings import get_buildings
from models import Building
 
# init the calendar
cal = Calendar()

# Some properties are required to be compliant
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')






from ics import Calendar
import requests
 
# Parse the URL
# url = "https://timetable.soton.ac.uk/Feed/Index/0_u1pM-A6BasrqTu_091Qi9Vl5jMCkLhC9JC09dY8TVH7_FPZmrl-PX9PTlt0UKwdjIfOBadbanQLrLzUbZhQw2"
# cal = Calendar(requests.get(url).text)
 
timetable = Calendar()

# Print all the events


events = []


def ImportCalanderFromLink(link):
    global timetable
    global events
    url = link
    timetable = Calendar(requests.get(url).text)
    events = timetable.events

def GetLecturesInBuilding(inpbuilding):
    NewEvents = []
    
    for x in events:
        if x.location != "":
            currentlocation = x.location.split(" ")
            building = currentlocation[0]
            room = currentlocation[2]
            if inpbuilding == building:
                NewEvents.append(x)
    
    return GetNextFiveLectures(NewEvents)


def GetLecturesInRoom(inpbuilding,inpRoom):
    NewEvents = []
    
    for x in events:
            
        if x.location != "":
            currentlocation = x.location.split(" ")
            building = currentlocation[0]
            room = currentlocation[2]
            if inpbuilding == building and inpRoom == room:
                NewEvents.append(x)
    return GetNextFiveLectures(NewEvents)


def GetNextFiveLectures(AllLectures: list):
    now = datetime.now(pytz.timezone('Europe/London'))
    AllLectures.sort(key=lambda x: x.begin)
    newLectures = []
    counter = 0
    currentindex = 0
    max = 5
    if len(AllLectures) < 5:
        max = len(AllLectures)
    while counter < max :
        if AllLectures[currentindex].begin.datetime.replace(tzinfo=pytz.timezone('Europe/London')) > now:
            counter = counter + 1
            newLectures.append(AllLectures[currentindex])
        currentindex = currentindex + 1  
    return newLectures

def GetLecturesToday():
    now = datetime.now(pytz.timezone('Europe/London'))
    now = datetime(year = 2024, month = 9, day = 30)
    TodaysLectures = []
    for x in events:
        if x.begin.datetime.year == now.year and x.begin.datetime.month == now.month and x.begin.datetime.day == now.day:
            TodaysLectures.append(x)
    return TodaysLectures

def GetLecturesForDate(timestamp: int):
    day = datetime.fromtimestamp(timestamp)
    TodaysLectures = []
    for x in events:
        if x.begin.datetime.year == day.year and x.begin.datetime.month == day.month and x.begin.datetime.day == day.day:
            TodaysLectures.append(x)
    return TodaysLectures
    
def GetTodaysBuildings() -> list[Building]:
    todays_lectures = GetLecturesToday()
    todays_lectures.sort(key=lambda x: x.begin)
    todays_buildings = []
    buildings = get_buildings()
    

    for lecture in todays_lectures:
        currentlocation = lecture.location.split(" ")
        building = buildings.get(currentlocation[0])
        if building is None:
            continue
        
        todays_buildings.append(building)
    return todays_buildings

def GetCoordsOfPathBetweenBuildings():
    url = "https://graphhopper.com/api/1/route"

    query = {
    "profile": "foot",
    "point": "string",
    "point_hint": "string",
    "snap_prevention": "string",
    "curbside": "any",
    "locale": "en",
    "elevation": "false",
    "details": "string",
    "optimize": "false",
    "instructions": "true",
    "calc_points": "true",
    "debug": "false",
    "points_encoded": "true",
    "ch.disable": "false",
    "heading": "0",
    "heading_penalty": "300",
    "pass_through": "false",
    "algorithm": "round_trip",
    "round_trip.distance": "10000",
    "round_trip.seed": "0",
    "alternative_route.max_paths": "2",
    "alternative_route.max_weight_factor": "1.4",
    "alternative_route.max_share_factor": "0.6",
    "key": "d9b5518a-081e-4dee-b025-af103674a28a"
    }

    response = requests.get(url, params=query)

    data = response.json()
    print(data)
    

ImportCalanderFromLink("https://timetable.soton.ac.uk/Feed/Index/0_u1pM-A6BasrqTu_091Qi9Vl5jMCkLhC9JC09dY8TVH7_FPZmrl-PX9PTlt0UKwdjIfOBadbanQLrLzUbZhQw2")