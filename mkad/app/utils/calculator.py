from mkad.app.data import MKAD_POLYGON_COORDS
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vincenty import vincenty
from mkad.app.helpers.input_checkers import isinside 



def calculate_distance_from_to(point:Point= None, polygon:Polygon= Polygon(MKAD_POLYGON_COORDS)) -> float:
    """This function calculates the distance, in km, from a location to a specified polygon. 
    \nThe calculation is based on the function vincenty. See https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    """
    # Input Validators
    if not isinstance(point, Point):
        raise ValueError(f'Expected type shapely.geometry.Point. Got {type(point)}')
    if not isinstance(polygon, Polygon):
        raise ValueError(f'Expected type shapely.geometry.polygon.Polygon. Got {type(polygon)}')

    # Checks if the point is inside the polygon
    if isinside(point, polygon):
        return 0.0

    nearest_point_coord = get_nearest_coords(polygon, point)
    point_coord= list(point.coords)[0]
    return round(vincenty(point_coord, nearest_point_coord), 2)
    

def get_nearest_coords(polygon:Polygon= None, point:Point= None) -> Point:
    """
    This function returns the polygon boundary point closest to the specified location point.
    """
    # Input Validators
    if not isinstance(point, Point):
        raise ValueError(f'Expected type shapely.geometry.Point. Got {type(point)}')
    if not isinstance(polygon, Polygon):
        raise ValueError(f'Expected type shapely.geometry.polygon.Polygon. Got {type(polygon)}')

    polygon_lat, polygon_lon= polygon.exterior.coords.xy
    polygon_coords= [tuple([polygon_lat[i], polygon_lon[i]]) for i in range(len(polygon_lat))]
    point_coord= list(point.coords)[0]
    return min(polygon_coords, key=lambda polygon_coord: vincenty(polygon_coord, point_coord))