import numpy as np
from shapely.geometry import Point, MultiPoint
from shapely.geometry.polygon import Polygon
from mkad.app.helpers import input_checkers

def generate_shapely_point(point:str= None) -> Point:
    """This function is designed to work directly with the type of geo-coordinate response that the Yandex api gives. 
    \nIt takes a string "Lon Lat" and transforms it into a Point(lat, lon).
    """

    # Input Validators
    if not isinstance(point, str):
        raise ValueError(f'Expected type str. Got {type(point)}')
    input_checkers.isvalidcoord(point)
    lon= float(point.split()[0])
    lat= float(point.split()[1])
    return Point(lat, lon)


def get_equidistant_points(p1:np.ndarray= None, p2:np.ndarray= None, parts:int= None):
    """This function is responsible for distributing equidistant points along a line.
    """

    # Input Validators
    if not isinstance(p1, np.ndarray):
        raise ValueError(f'Expected type np.ndarray. Got {type(p1)}')
    if not isinstance(p2, np.ndarray):
        raise ValueError(f'Expected type np.ndarray. Got {type(p2)}')
    if not isinstance(parts, int):
        raise ValueError(f'Expected type int. Got {type(parts)}')

    return zip(np.linspace(p1[0], p2[0], parts+1),
               np.linspace(p1[1], p2[1], parts+1))


def redistribute_vertices(vertices:np.ndarray= None, parts:int= 200) -> np.ndarray:
    """This function is responsible for the distribution of equidistant points along the lines that compose the polygon boundary.
    """

    # Input Validators
    if not isinstance(vertices, np.ndarray):
        raise ValueError(f'Expected type np.ndarray. Got {type(vertices)}')
    if not isinstance(parts, int):
        raise ValueError(f'Expected type int. Got {type(parts)}')

    redistributed_vertices_array= np.empty((0,2), float)
    for idx in range(len(vertices)-1):
        equidistant_points= np.array(
                                list(get_equidistant_points(
                                    vertices[idx],
                                    vertices[idx+1], 
                                    parts
                                ))
                            )
        redistributed_vertices_array= np.append(redistributed_vertices_array,equidistant_points)

    redistributed_vertices_array= redistributed_vertices_array.reshape(int(len(redistributed_vertices_array)/2),2)
    redistributed_vertices_array = [tuple(row) for row in redistributed_vertices_array]

    return np.unique(redistributed_vertices_array, axis=0)

def build_address(args:dict= None) -> str:
    """This function transforms a dictionary with the address into a string, which represents the same information.
    """
    
    # Input Validators
    if not isinstance(args, dict):
        raise ValueError(f'Expected type dict. Got {type(args)}')

    _parts= [
        args.country, 
        ", ".join(args.provinces) if args.provinces else "",
        args.area,
        args.locality,
        args.street,
        args.house
        ]

    parts=list()
    for p in _parts:
        if p:
            # Input Validators
            input_checkers.has_special_char(p)
            parts.append(p)

    return  ", ".join(parts)


def build_polygon(lonlat_list:list= None) -> Polygon:

    points= list()
    for lonlat in lonlat_list:
        points.append(generate_shapely_point(lonlat))
    
    polygon= MultiPoint(points).convex_hull


    #Input validator
    input_checkers.isvalidpolygon(polygon)

    new_points= redistribute_vertices(np.array(polygon.exterior.coords))
    return MultiPoint(new_points).convex_hull