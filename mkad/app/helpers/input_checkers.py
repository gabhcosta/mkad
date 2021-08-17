import logging
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask_restful import abort


def has2arguments(args:dict= None) -> None:
     """
     Checks whether a dictionary has at least 3 non-null values in key:value pairs. 
     If the dictionary is not valid, throws an HTTPException 400.
     """
     
     # Input Validators  
     if not isinstance(args, dict):
          raise ValueError(f'Expected type shapely.geometry.Point. Got {type(args)}')

     counter= 0
     for _, v in args.items():
          if not counter <=2:
               logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
               abort(400, status_code='400', error='MinArguments', message= 'Need more than 2 agurments.')
          if not v:
               counter+=1


def isbiggerthanzero(found:list= None) -> None:
     """
     Checks if the list is non-empty "[]" and if its first value is greater than 0.
     If the list is not valid, throws an HTTPException 404.
     """

     # Input Validators  
     if not isinstance(found, list):
          raise ValueError(f'Expected type shapely.geometry.Point. Got {type(found)}')     

     if found and int(found[0]) == 0:
          logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
          abort(404, status_code='404', error='ResourceDoesNotExist', message= 'Could not find location.')
          

def haserror(error:list= None) -> None:
     """
     Checks if the list exists, if it does, throws the exception which must be in the first position of the list.
     """

     # Input Validators  
     if not isinstance(error, list):
          raise ValueError(f'Expected type shapely.geometry.Point. Got {type(error)}')   

     if error:
          logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
          abort(error[0], message= 'Unexpected problem, probably some external resource is unreachable. Please, contact us.' )


def isinside(point:Point= None, polygon:Polygon= None) -> bool:
     """
     Check if the point belongs to the polygon. If it is on the border or inside it returns True.
     Consider that the Point and the Polygon are Shapely objects.
     """

     # Input Validators
     if not isinstance(point, Point):
          raise ValueError(f'Expected type shapely.geometry.Point. Got {type(point)}')
     if not isinstance(polygon, Polygon):
          raise ValueError(f'Expected type shapely.geometry.polygon.Polygon. Got {type(polygon)}')

     return polygon.contains(point) or polygon.touches(point) or point.within(polygon)


def has_special_char(string:str= None, special_charstring:str= "!@#$\\%^&*()-+?_=<>/") -> None:
     if any(c in special_charstring for c in string):
          logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
          abort(400, status_code='400', error='SpecCharNotAllowed', message= 'The request contains a special character that is not allowed.')


def isvalidcoord(point:str= None) -> None:
     error = False
     try:
          if len(point.split()) > 2:
               error= True
          _lon= float(point.split()[0])
          _lat= float(point.split()[1])
     except:
          error= True
     else:
          if _lon > 180 or _lon < -180:
               error= True
          if _lat > 90 or _lat < -90:
               error= True
     finally:
          if error:
               logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
               abort(400, status_code='400', error='InvalidCoords', message= f'The request contains an invalid coord {point}.')


def has_len_shorter_than(obj_list:list= None, maxlen:int= 20) -> None:

     if not len(obj_list) <= maxlen:
          logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
          abort(400, status_code='400', error='MaxCoordsExceeded', message= f'The request too many coords, maximum allowed is {maxlen}.')


def isvalidpolygon(polygon:Polygon= None) -> None:
     if not polygon.is_valid or not isinstance(polygon, Polygon):
          logging.info(f"{'-' * 42} END OF REQUEST {'-' * 46}")
          abort(400, status_code='400', error='InvalidCoords', message= 'The request has points that do not form a valid polygon.')
