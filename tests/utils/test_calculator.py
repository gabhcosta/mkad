from mkad.app.data import MKAD_POLYGON_COORDS
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from mkad.app.utils import calculator

def test_calculate_distance_from_to():

    result= calculator.calculate_distance_from_to(Point(-27.581393, -48.618189), Polygon(MKAD_POLYGON_COORDS))
    expected= 12253.91

    assert result == expected
    

def test_get_nearest_coords():

    result= calculator.get_nearest_coords(Polygon(MKAD_POLYGON_COORDS), Point(-27.581393, -48.618189))
    expected= (55.71250405810921, 37.38676828708327)
    
    assert result == expected