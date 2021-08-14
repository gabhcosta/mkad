import logging
from mkad.app.utils import KeyResearcher
from mkad.app.utils.calculator import calculate_distance_from_to
from mkad.app.helpers.data_manipulation import  generate_shapely_point

researcher = KeyResearcher()

def handle_yandex_response(r):
    point= researcher.search_in(r.json(), 'Point')
    address= researcher.search_in(r.json(), 'formatted')
    if len(point) == 1 and len(address) ==1:
        result= {
                    'Response Status': 'Exact',
                    'Point [lon  lat]': point[0]['pos'],
                    'Address Found': address[0],
                    'Distance from MKAD': f"{calculate_distance_from_to(generate_shapely_point(point[0]['pos']))} km"
                }
        logging.info(f"---> Response Status: Exact")
        logging.info(f"---------> Point: {result['Point [lon  lat]']} Distance from MKAD: {result['Distance from MKAD']}")
    else:   
        result= {'Response Status': 'Inaccurate',}
        logging.info(f"---> Response Status: Inaccurate")
        for i in range(len(point)):
            result[i] =  {
                                'Point [lon  lat]': point[i]['pos'],
                                'Address Found': address[i],
                                'Distance from MKAD': f"{calculate_distance_from_to(generate_shapely_point(point[i]['pos']))} km"
                            }
            logging.info(f"---------> Point [lon  lat]: {result[i]['Point [lon  lat]']} Distance from MKAD: {result[i]['Distance from MKAD']}")
    return result