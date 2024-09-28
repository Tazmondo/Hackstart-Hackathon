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

ImportCalanderFromLink("https://timetable.soton.ac.uk/Feed/Index/0_u1pM-A6BasrqTu_091Qi9Vl5jMCkLhC9JC09dY8TVH7_FPZmrl-PX9PTlt0UKwdjIfOBadbanQLrLzUbZhQw2")