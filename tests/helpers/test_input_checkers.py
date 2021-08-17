from mkad.app.helpers import input_checkers, data_manipulation
from flask_restful import HTTPException
from shapely.geometry import Point, MultiPoint
from shapely.geometry.polygon import Polygon
from mkad.app.data import MKAD_POLYGON_COORDS

def test_has2arguments():
    args = {
    "country": "",
    "provinces": "",
    "area":"",
    "locality":"",
    "street": "",
    "house": ""
    }

    try:
        input_checkers.has2arguments(args)
    except Exception as e:
        assert isinstance(e, HTTPException)


def test_isbiggerthanzero():
    found= ['0']

    try:
        input_checkers.isbiggerthanzero(found)
    except Exception as e:
        assert isinstance(e, HTTPException)


def test_haserror():
    error= [404]
    try:
        input_checkers.haserror(error)
    except Exception as e:
        assert isinstance(e, HTTPException)

def test_isinside():
    point= Point(55.734618, 37.602624)
    point2= Point(37.602624, 55.734618)
    polygon= Polygon(MKAD_POLYGON_COORDS)
    
    result1= input_checkers.isinside(point, polygon)
    expected1= True
    
    result2= input_checkers.isinside(point2, polygon)
    expected2= False

    assert result1 == expected1
    assert result2 == expected2

def test_as_special_char():
    string='sadhuashdsaiudha&sadihas'

    try:
        input_checkers.has_special_char(string)
    except Exception as e:
        assert isinstance(e, HTTPException)


def test_isvalidcoord():
    point=["-1873 -8741"]

    try:
        input_checkers.isvalidcoord(point)
    except Exception as e:
        assert isinstance(e, HTTPException)


def test_has_len_shorter_than():
    points=["-1873 -8741", "-1873 -8741", "-1873 -8741" ]

    try:
        input_checkers.has_len_shorter_than(points, 2)
    except Exception as e:
        assert isinstance(e, HTTPException)
    

def test_isvalidpolygon():
    lonlat_list= ["-80.40604412766334 12.694830944052345", "-81.63651287766334 -56.5771338389153"]
    points= list()
    for lonlat in lonlat_list:
        points.append(data_manipulation.generate_shapely_point(lonlat))
    
    polygon= MultiPoint(points).convex_hull

    try:
        input_checkers.isvalidpolygon(polygon)
    except Exception as e:
        assert isinstance(e, HTTPException)
    
    
    
