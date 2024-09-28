import csv

from models import Building



with open("buildings.csv", "r") as f:
    csvbuildings = csv.reader(f)
    buildings = dict()
    firstline = True
    for row in csvbuildings:
        try:
            building = Building(number=row[0], name=row[1], latitude=float(row[4]), longitude=float(row[5]))
            buildings[building.number] = building
        except ValueError:
            pass

def get_buildings() -> dict[str, Building]:
    return buildings
