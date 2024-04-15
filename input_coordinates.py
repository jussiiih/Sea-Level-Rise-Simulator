from pyproj import Proj, transform
import math

def lat_lon_to_utm(latitude, longitude, zone):
    '''Transform latitude and logitude git pullcoordinates into UTM coordinates'''
    utm_proj_str = f'+proj=utm +zone={zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    wgs84_proj_str = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    
    # Define projection objects
    utm_proj = Proj(utm_proj_str)
    wgs84_proj = Proj(wgs84_proj_str)
    
    # Transform latitude and longitude to UTM
    easting, northing = transform(wgs84_proj, utm_proj, longitude, latitude)
    return [northing, easting]

def transform_coordinates(latitude, longitude, zoom):
    '''Transforms 2 coordinates and creates an area around them'''
    #Transforms real coordinates into coordinates that National Land Survey of Finland's API uses
    utm_latitude, utm_longitude = lat_lon_to_utm(latitude, longitude, 35)

    # Calculate the area around the coordinates
    y = math.floor(750.0 / int(zoom))
    x = math.floor(750.0 / int(zoom))
    western = utm_longitude - x
    eastern = utm_longitude + x
    southern = utm_latitude - y
    northern = utm_latitude + y

    # changing the coordinates to strings, making sure they are not too long
    western = str(western)[:10]
    eastern = str(eastern)[:10]
    southern = str(southern)[:10]
    northern = str(northern)[:10]

    return [western, eastern, southern, northern]


def input_coordinates():
    '''Asks user the coordinates for their area of interest'''

    # Give instructions to the user
    print("What is the area you are intrested in?")
    print("Input the coordinates for latitude and longitude.")

    
    # Ask latitude and longitude as input
    latitude = float(input("Input latitude: "))
    longitude = float(input("Input longitude: "))

    coordinates = transform_coordinates(latitude, longitude)
    return coordinates