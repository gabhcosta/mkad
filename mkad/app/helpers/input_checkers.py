import logging
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask_restful import abort


def has2arguments(args:dict= None) -> None:
     """
     Checks whether a dictionary has at least 3 non-null values in key:value pairs. 
     If the dictionary is not valid, throws an HTTPException 400.
     """

     counter= 0
     for _, v in args.items():
          if not counter <=2:
               logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
               abort(400, status_code='400', error='MinArguments', message= 'Need more than 2 agurments.')
          if not v:
               counter+=1


def isbiggerthanzero(found:list= None) -> None:
     """
     Checks if the list is non-empty "[]" and if its first value is greater than 0.
     If the list is not valid, throws an HTTPException 404.
     """     

     if found and int(found[0]) == 0:
          logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
          abort(404, status_code='404', error='ResourceDoesNotExist', message= 'Could not find location.')
          

def haserror(error:list= None) -> None:
     """
     Checks if the list exists, if it does, throws the exception which must be in the first position of the list.
     """
     
     if error:
          logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
          abort(error[0], message= 'Unexpected problem, probably some external resource is unreachable. Please, contact us.' )


def isinside(point:Point= None, polygon:Polygon= None) -> bool:
     """
     Check if the point belongs to the polygon. If it is on the border or inside it returns True.
     Consider that the Point and the Polygon are Shapely objects.
     """
     return polygon.contains(point) or polygon.touches(point) or point.within(polygon)




