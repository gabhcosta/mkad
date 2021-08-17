import os
import numpy as np
import pandas as pd
from mkad.app.helpers.data_manipulation import redistribute_vertices

_mkad_coords_file_path= os.path.join(os.path.dirname(os.path.abspath(__file__)),'mkad_coordinates.csv')
_mkad_coords_from_file= pd.read_csv(_mkad_coords_file_path, dtype='str').to_numpy(dtype=np.longdouble)

MKAD_POLYGON_COORDS= redistribute_vertices(_mkad_coords_from_file, 200)

