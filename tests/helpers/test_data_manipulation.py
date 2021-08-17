from mkad.app.helpers import data_manipulation
from shapely.geometry import Point, MultiPoint
from mkad.app.data.test_data import new_points
import numpy as np

def test_generate_shapely_point():

    result= data_manipulation.generate_shapely_point('1 0').xy
    expected= Point(0, 1).xy

    assert result == expected

def test_get_equidistant_points():

    result= list(data_manipulation.get_equidistant_points(np.array([0,0]), np.array([10,10]), 4))
    expected= [(0.0, 0.0), (2.5, 2.5), (5.0, 5.0), (7.5, 7.5), (10.0, 10.0)]

    assert result == expected

def test_redistribute_vertices():

    result= data_manipulation.redistribute_vertices(np.array([[0,0], [10,10]]), 4)
    expected= np.array([(0.0, 0.0), (2.5, 2.5), (5.0, 5.0), (7.5, 7.5), (10.0, 10.0)])

    assert (result == expected).all()

def test_build_address():
    class Args(dict):
        country= "Russia"
        provinces= ["Tsentralny federalny okrug", "Moscow"]
        area= ""
        locality= "Moscow"
        street= "Krymskaya Embankment"
        house= "10к1"

    args = Args()

    result= data_manipulation.build_address(args)
    expected= 'Russia, Tsentralny federalny okrug, Moscow, Moscow, Krymskaya Embankment, 10к1'
    
    assert result == expected


def test_build_polygon():
    lonlat_list= ["-80.40604412766334 12.694830944052345", "-81.63651287766334 -56.5771338389153", 
    "-29.95682537766334 -56.38299200927733", "-32.59354412766334 13.208756628211567"]
    
    result= data_manipulation.build_polygon(lonlat_list)
    expected= MultiPoint(new_points).convex_hull

    assert result==expected