# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz
 
# init the calendar
cal = Calendar()

# Some properties are required to be compliant
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')




# # Write to disk
# directory = Path.cwd() / 'MyCalendar'
# try:
#    directory.mkdir(parents=True, exist_ok=False)
# except FileExistsError:
#    print("Folder already exists")
# else:
#    print("Folder was created")
 
# f = open(os.path.join(directory, 'example.ics'), 'wb')
# f.write(cal.to_ical())
# f.close()






# e = open('MyCalendar/example.ics', 'rb')
# ecal = Calendar.from_ical(e.read())
# for component in ecal.walk():
#    print(component.name)
# e.close()



# e = open('MyCalendar/example.ics', 'rb')
# ecal = Calendar.from_ical(e.read())
# for component in ecal.walk():
#    if component.name == "VEVENT":
#        print(component.get("name"))
#        print(component.get("description"))
#        print(component.get("organizer"))
#        print(component.get("location"))
#        print(component.decoded("dtstart"))
#        print(component.decoded("dtend"))
# e.close()



from ics import Calendar
import requests
 
# Parse the URL
url = "https://timetable.soton.ac.uk/Feed/Index/0_u1pM-A6BasrqTu_091Qi9Vl5jMCkLhC9JC09dY8TVH7_FPZmrl-PX9PTlt0UKwdjIfOBadbanQLrLzUbZhQw2"
cal = Calendar(requests.get(url).text)
 
timetable = Calendar()

# Print all the events


inpbuilding = input("Enter the building")
inproom = input("enter the room")



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
    now = datetime.now()
    AllLectures.sort(key=lambda x: x.begin)
    newLectures = []
    counter = 0
    currentindex = 0
    while counter < 5 :
        if AllLectures[currentindex].begin.datetime > now and counter < 5:
            counter = counter + 1
            newLectures.append(AllLectures[currentindex])
        currentindex = currentindex + 1  
    return newLectures

ImportCalanderFromLink("https://timetable.soton.ac.uk/Feed/Index/0_u1pM-A6BasrqTu_091Qi9Vl5jMCkLhC9JC09dY8TVH7_FPZmrl-PX9PTlt0UKwdjIfOBadbanQLrLzUbZhQw2")
print(GetLecturesInBuilding(inpbuilding))