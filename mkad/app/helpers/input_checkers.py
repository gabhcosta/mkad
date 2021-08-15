from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from flask_restful import abort


def has2arguments(args):
     counter= 0
     for _, v in args.items():
          if not counter <=2:
               abort(400, status_code='400', error='MinArguments', message= 'Need more than 2 agurments.')
          if not v:
               counter+=1

def has1location(found):
     if found and int(found[0]) == 0:
          abort(404, status_code='404', error='ResourceDoesNotExist', message= 'Could not find location.')
          

def haserror(error):
     if error:
          abort(error[0], message= 'Unexpected problem, probably some external resource is unreachable. Please, contact us.' )

def isinside(point, polygon):
     return polygon.contains(point) or polygon.touches(point) or point.within(polygon)




