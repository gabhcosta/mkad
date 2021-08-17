import logging
from mkad.app.data import MKAD_POLYGON_COORDS
from shapely.geometry import MultiPoint
from shapely.geometry.polygon import Polygon
from werkzeug.sansio.response import Response
from mkad.app.utils import KeyResearcher
from mkad.app.utils.calculator import calculate_distance_from_to
from mkad.app.helpers.data_manipulation import  generate_shapely_point
from mkad.app.helpers import input_checkers
from requests import Response

researcher = KeyResearcher()

def generate_response(r:Response= None, polygon:Polygon= MultiPoint(MKAD_POLYGON_COORDS).convex_hull) -> dict:
    """ This function is responsible for interpreting the response from the Yandex api and returning the appropriate response. 
    If Yandex doesn't return any locale or returns an error, the input validators will generate an error. 
    If this method can interpret the answer correctly, it returns a single answer (Exact), if Yandex returns only one location,
    otherwise it returns several answers (Inaccurate, limit 10) for all the locations that Yandex returned.
    """

    # Input Validators
    if not isinstance(r, Response):
      raise ValueError(f'Expected type requests.Response. Got {type(r)}')
    input_checkers.isbiggerthanzero(researcher.search_in(r.json(), 'found'))
    input_checkers.haserror(researcher.search_in(r.json(), 'statusCode'))

    point= researcher.search_in(r.json(), 'Point')
    address= researcher.search_in(r.json(), 'formatted')

    # Exact, it means that Yandex returned only 1 locality
    if len(point)==1 and len(address) ==1:
        result= {
                    'Response Status': 'Exact',
                    'Point [lon  lat]': point[0]['pos'],
                    'Address Found': address[0],
                    'Distance from MKAD': f"{calculate_distance_from_to(generate_shapely_point(point[0]['pos'], polygon))} km"
                }
        logging.info(f"---> Response Status: Exact")
        logging.info(f"---------> Point: {result['Point [lon  lat]']} Distance from MKAD: {result['Distance from MKAD']}")

    # Inaccurate, it means that Yandex returned more than 1 locality
    else:   
        result= {'Response Status': 'Inaccurate',}
        logging.info(f"---> Response Status: Inaccurate")
        for i in range(len(point)):
            result[i] =  {
                                'Point [lon  lat]': point[i]['pos'],
                                'Address Found': address[i],
                                'Distance from MKAD': f"{calculate_distance_from_to(generate_shapely_point(point[i]['pos']), polygon)} km"
                            }
            logging.info(f"---------> Point [lon  lat]: {result[i]['Point [lon  lat]']} Distance from MKAD: {result[i]['Distance from MKAD']}")
    return result