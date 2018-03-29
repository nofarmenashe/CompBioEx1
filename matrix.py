import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

matrix_dims = (10, 10)
color_map = colors.ListedColormap(['white', 'red', 'green'])


def convert_matrix(dims, algo_matrix):
    m = np.zeros(dims)
    for i in range(dims[0]):
        for j in range(dims[1]):
            if algo_matrix[i][j] is None:
                m[i, j] = 1
            elif not algo_matrix[i][j]:
                m[i, j] = 2
            else:
                m[i, j] = 3
    return m

algo_matrix = [[True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None],
               [True, False, None, None, None, True, False, None, None, None]]
plt.matshow(convert_matrix(matrix_dims, algo_matrix), cmap=color_map)
patches = [ ) ]
plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
plt.grid(True)

plt.show()
