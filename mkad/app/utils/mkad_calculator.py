import pandas as pd #temporary
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


df= pd.read_csv(r'C:\Users\gabri\Desktop\MKAD\mkad\mkad\app\data\mkad_coordinates.csv') #temporary
coords= df.to_numpy()
polygon= Polygon(coords)
point = Point(55.62843206524178, 37.47188988957678)
print(polygon.contains(point)) # check if polygon contains point
print(point.within(polygon)) # check if a point is in the polygon 
print(polygon.touches(point)) # check if point lies on border of polygon 