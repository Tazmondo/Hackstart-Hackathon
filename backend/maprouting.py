import ical
import requests

def GetCoordsOfPathBetweenBuildings():
    url = "https://graphhopper.com/api/1/route"

    buildingLocations = ical.GetTodaysBuildings()
    coordsOfBuildings = ""
    counter = 0
    for x in buildingLocations:
        coordsOfBuildings = coordsOfBuildings + "point=" + str(x.latitude) + "," + str(x.longitude)
        if counter < len(buildingLocations) - 1:
            coordsOfBuildings = coordsOfBuildings + "&"
        counter = counter + 1

    print(coordsOfBuildings)
    query = {
    "profile": "foot",
    "point": ["point=11.324,12.4443", "point=11,12.1"],
    "curbside": "any",
    "locale": "en",
    "elevation": "false",
    "optimize": "false",
    "instructions": "true",
    "calc_points": "true",
    "debug": "false",
    "points_encoded": "true",
    "ch.disable": "false",
    "heading": "0",
    "heading_penalty": "300",
    "pass_through": "false",
    "key": "d9b5518a-081e-4dee-b025-af103674a28a"
    }

    response = requests.get(url, params=query)

    data = response.json()
    print(data)

GetCoordsOfPathBetweenBuildings()