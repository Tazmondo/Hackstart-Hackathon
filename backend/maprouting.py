import ical
import requests
from graphh import GraphHopper

def GetCoordsOfPathBetweenBuildings():
    url = "https://graphhopper.com/api/1/route"

    buildingLocations = ical.GetTodaysBuildings()
    coordsOfBuildings = []
    counter = 0
    for x in buildingLocations:
        coordsOfBuildings.append(( x.latitude  ,  x.longitude ))
        counter = counter + 1

    print(coordsOfBuildings)

    mapper = GraphHopper("d9b5518a-081e-4dee-b025-af103674a28a")

    t = mapper.address_to_latlong("Poole")
    print(t)
    routing = mapper.route(coordsOfBuildings)
    mapper.ro
    print(routing)


GetCoordsOfPathBetweenBuildings()