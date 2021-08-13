from mkad.app.data import MKAD_POLYGON_COORDS
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vincenty import vincenty



#need to round the coords
#need to check the point difference precision
polygon= Polygon(MKAD_POLYGON_COORDS)
point = Point(55.86914780988667, 37.80815305728345) #need to truncate point 55.6624094603668 37.4324506882218
print(polygon.contains(point)) # check if polygon contains point
print(point.within(polygon)) # check if a point is in the polygon 
print(polygon.touches(point)) # check if point lies on border of polygon 
print(point.distance(polygon))

def calculate_distance_from_polygon(polygon: Polygon, point: Point):
    nearest_point_coord = get_nearest_coords_from_the_polygon(polygon, point)
    point_coord= list(point.coords)[0]
    return round(vincenty(point_coord, nearest_point_coord), 2)
    


def get_nearest_coords_from_the_polygon(polygon, point):
    polygon_lat, polygon_lon= polygon.exterior.coords.xy
    polygon_coords= [tuple([polygon_lat[i], polygon_lon[i]]) for i in range(len(polygon_lat))]
    point_coord= list(point.coords)[0]
    return min(polygon_coords, key=lambda polygon_coord: vincenty(polygon_coord, point_coord))



print(calculate_distance_from_polygon(polygon, point))