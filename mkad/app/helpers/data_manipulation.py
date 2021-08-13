import numpy as np


def get_equidistant_points(p1, p2, parts):
    return zip(np.linspace(p1[0], p2[0], parts+1),
               np.linspace(p1[1], p2[1], parts+1))


def redistribute_vertices(vertices, parts):
    redistributed_vertices_array= np.empty((0,2), float)

    for idx in range(len(vertices)-1):
        equidistant_points= np.array(
                                list(get_equidistant_points(
                                    vertices[idx],
                                    vertices[idx+1], 
                                    parts
                                ))
                            )
        redistributed_vertices_array= np.append(redistributed_vertices_array,equidistant_points)

    redistributed_vertices_array= redistributed_vertices_array.reshape(int(len(redistributed_vertices_array)/2),2)
    redistributed_vertices_array = [tuple(row) for row in redistributed_vertices_array]

    return np.unique(redistributed_vertices_array, axis=0)