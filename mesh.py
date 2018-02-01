#!/usr/bin/env python

""" Defines MeshGrid and MeshCell classes to sub-divide a geometry
into a computional domain via grid generation.

"""

import matplotlib.pyplot as plt
import numpy as np

from geometry import create_spacecraft_geometry


class MeshGrid(object):
    """
    """

    def __init__(self):
        """
        """
        pass

#        resolution_x
#        resolution_y
#        # Specify boundary cells
#        cells_top
#        cells_bottom
#        cells_left
#        cells_right
#
#        # Specify interior cells
#        cells_interior
#
#        construct_grid_from_geometry()
#        visualize()
#        visualize_colormap(u or T or p or etc..)


class MeshCell(object):
    """
    """

#    def __init__(self):
#        """
#        """
#        pass
#
#    x, y, ID
#
#    rho, u, T, p, etc...
#    rho_old, u_old, T_old, p_old, etc...
#
#    get_left_neighbor()
#    get_right_neighbor()
#    get_top_neighbor()
#    get_bottom_neighbor()


def algebraic_structured_mesh(geometry):
    """Develop a structured mesh using the simple algebraic method.
    """

    IL = 200
    JL = 200

    xmax = max(geometry.x_vector)
    xmin = min(geometry.x_vector)

    beta = 1.5
    zeta = beta + 1
    gamma = beta - 1
    alpha = zeta / gamma

    height_vector = geometry.y_vector_top - geometry.y_vector_bottom

    xi = np.linspace(xmin, xmax, num=IL)
    eta = np.linspace(0, 1, num=JL)

    y_final = np.zeros((IL, JL))

    for idx in np.arange(0, IL):
        for jdx in np.arange(0, JL):
            chi = 1 - eta[jdx]
            y_final[idx, jdx] = (height_vector[idx] * (zeta - gamma * alpha **
                                                       chi) / (alpha ** chi + 1)) + geometry.y_vector_bottom[idx]

    y_combined = np.concatenate((np.fliplr(-y_final[:, 1:]), y_final), axis=1)
    x_combined = y_combined.copy()

    JL_NEW = y_combined.shape[1]
    for j in np.arange(0, JL_NEW):
        x_combined[:, j] = xi

    fig, ax = plt.subplots(figsize=(12, 9))

    plt.plot(x_combined, y_combined, zorder=1, alpha=0.9, color='k')

    textstr = 'IL: {} \nJL: {} \nbeta: {}'.format(IL, JL_NEW, beta)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='#FF5733', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', bbox=props)

    plt.autoscale(axis='both', tight=False)
    plt.margins(0.01, 0.01)
    plt.xlabel('x [m]', fontsize=14)
    plt.ylabel('y [m]', fontsize=14)
    plt.title('Geometry Mesh', fontsize=20)
    plt.subplots_adjust(top=0.925)

    return


if __name__ == "__main__":
    pass
    sc = create_spacecraft_geometry()
    algebraic_structured_mesh(sc)
