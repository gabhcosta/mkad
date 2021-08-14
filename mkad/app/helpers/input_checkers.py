from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def isinside(point, polygon):
     return polygon.contains(point) or polygon.touches(point) or point.within(polygon)




