from mkad.app.helpers import input_checkers
from flask_restful import HTTPException
from shapely.geometry import Point
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


def test_has1location():
    found= ['0']

    try:
        input_checkers.has1location(found)
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