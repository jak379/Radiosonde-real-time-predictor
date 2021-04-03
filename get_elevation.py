#Get elevation module
#
#
# Main features: 
#   - Mapbox is damn fast
#   - auto buffering
#   - offline functionality
#
#Usage:
#from get_elevation import getElevation
#ele = getElevation(x, y)



import os
import json

#Documentation:
#https://docs.mapbox.com/help/glossary/access-token/
configuration = json.load(open('configuration.json',))
os.environ['MAPBOX_ACCESS_TOKEN'] = configuration["mapbox_token"]

import math
import numpy as np

import mapbox
from mapbox import Maps
import mapbox_vector_tile
from shapely.geometry import Point, Polygon

maps = Maps()

tilesFolder = configuration["mapbox_tiles_folder"]
if not os.path.exists(tilesFolder):
    os.makedirs(tilesFolder)

#Coppied from article (link down below)
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = (lon_deg + 180.0) / 360.0 * n
  ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def pathForTile(x, y, zoom):
    return (tilesFolder + '/' + str(x) + '-' + str(y) + '-' + str(zoom) + '.mvt')

#Change only if you know what are you doing! :)
zoom = 14
tileSizes = (0.087890625, 0.041528857421875) #Calculated from a chart in this article based on your zoom value (Im too lazy to do it autmatically): https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
loadedTiles = []

def requestTile(coords):
    global loadedTiles
    
    for l in loadedTiles:
        if l['x'] == coords[0] and l['y'] == coords[1]:
            return l['data']
    
    requestedTile = ""
    if not os.path.isfile(pathForTile(coords[0], coords[1], zoom)):
        print("MAPBOX> Requesting new tile:", coords[0], coords[1], zoom)
        response = ""
        while True:
            response = maps.tile("mapbox.mapbox-terrain-v2", coords[0], coords[1], zoom, file_format="mvt")
            if response.status_code == 200: #RESPONSE OK
                break
            else:
                print("MAPBOX> Request failed:", response.status_code, response.text, "... trying again!")
        with open(pathForTile(coords[0], coords[1], zoom), "wb") as output:
            output.write(response.content)
            
    with open(pathForTile(coords[0], coords[1], zoom), 'rb') as f:
        data = f.read()
    decoded_data = mapbox_vector_tile.decode(data)
    
    loadedTiles.append({'x': coords[0], 'y': coords[1], 'data': decoded_data})
    return decoded_data

def getElevation(x, y):
    coords = deg2num(x, y, zoom)
    tile = requestTile((int(coords[0]), int(coords[1])))
    tileplus = (int(coords[0]) + 1, int(coords[1]) + 1)
    limitCoords = (num2deg(int(coords[0]), int(coords[1]), zoom), num2deg(int(coords[0]+1), int(coords[1])+1, zoom))
    
    substractCoords = (limitCoords[0][0] - limitCoords[1][0], limitCoords[0][1] - limitCoords[1][1])
    substractCoordsActual = (limitCoords[0][0] - x, limitCoords[0][1] - y)
    
    extent = int(tile["contour"]["extent"])
    
    #Yeah I was lazy to find actual formula so I used direct proportion, works perfectly btw. :)
    coordsPercentage = (substractCoordsActual[0] / substractCoords[0], substractCoordsActual[1] / substractCoords[1])
    localCoords = (int(coordsPercentage[0] * extent), int(coordsPercentage[1] * extent))
    
    """
    print("limits", limitCoords)
    print("substractCoords", substractCoords)
    print("substractCoordsActual", substractCoordsActual)
    print("%", coordsPercentage)
    print("calculated pos", localCoords)
    """
    
    #Converting to shapely point
    point = Point(localCoords[0], localCoords[1])
    
    elevation = 0
    for c in tile["contour"]["features"]:
        #print("new Geometry - height:", c["properties"]["ele"])
        for d in c["geometry"]["coordinates"]:
            try:
                polygon = Polygon(d)
                #print("point", point, "polygon", polygon)
                inside = polygon.contains(point)
                if inside:
                    elevation = c["properties"]["ele"]
            except Exception as e:
                pass #Polygons with 2 or less points are not considered as polygons by shapely lib
    return elevation
   
#Verifying functionality   

"""
def test():
    inp = {'x': 50.74, 'y': 15.73}
    print("Elevation for coords", inp, "is:", getElevation(inp['x'], inp['y']))

#tile = requestTile(49.310, 17.654)
#tile = requestTile(49.310, 17.653)
#print(json.dumps(tile, indent=4, sort_keys=True))

test()
"""