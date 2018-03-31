import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, patches as mpatches, animation


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


def get_display_matrix(ax, algo_matrix):
    color_map = {1: 'red', 2: 'white', 3: 'green'}
    labels = {1: 'fire', 2: 'empty', 3: 'tree'}

    mat_show = ax.matshow(convert_matrix(dims, algo_matrix), cmap=colors.ListedColormap(color_map.values()))

    patches = [mpatches.Patch(color=color_map[i], label=labels[i]) for i in color_map]
    plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.005),
               fancybox=True, shadow=True, ncol=3)

    plt.xticks(np.arange(0.5, dims[1] + .5), [])
    plt.yticks(np.arange(0.5, dims[0] + .5), [])
    plt.grid(True)

    return mat_show


def animate(data):
        global grid

        newGrid =

        # update data
        mat.set_data(convert_matrix(dims, newGrid))
        grid = newGrid
        return [mat]

# testing - remove after create call from main file
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
dims = (10, 10)
grid = np.array(algo_matrix)
fig, ax = plt.subplots()
mat = get_display_matrix(ax, grid)
anim = animation.FuncAnimation(fig, animate, frames=200,
                        interval=800)
plt.show()
