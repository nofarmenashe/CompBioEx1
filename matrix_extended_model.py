import copy
import random
import numbers
import decimal
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, patches as mpatches, animation
from matplotlib.colors import same_color

dims = (0, 0)
grid = np.zeros(dims)
treeProb, fireProb, lightningProb, growProb = 0, 0, 0, 0
scorchedDays = 10


def convert_matrix(dims, algo_matrix):
    m = np.zeros(dims)
    for i in range(dims[0]):
        for j in range(dims[1]):
            if algo_matrix[i][j] is None:
                m[i, j] = 2

            elif not algo_matrix[i][j]:
                m[i, j] = 1

            # Scorched
            elif algo_matrix[i][j] is True:
                m[i, j] = 3

            # Scorched
            else:
                m[i, j] = 4
    return m


def get_display_matrix(dims, ax, algo_matrix):
    color_map = {1: 'red', 2: 'white', 3: 'green', 4: [1, 0.94, 0.901]}
    labels = {1: 'fire', 2: 'empty', 3: 'tree', 4: "scorched"}
    mat_show = ax.matshow(convert_matrix(dims, algo_matrix), vmin=1, vmax=4, cmap=colors.ListedColormap(color_map.values()), aspect="auto")
    patches = [mpatches.Patch(color=color_map[i], label=labels[i]) for i in color_map]
    plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.005),
               fancybox=True, shadow=True, ncol=4)

    plt.xticks(np.arange(0.5, dims[1] + .5), [])
    plt.yticks(np.arange(0.5, dims[0] + .5), [])
    plt.grid(True)

    return mat_show


def animate(data):
        global grid
        newGrid = iterate_over_forest(grid, dims[0], dims[1], fireProb, lightningProb, growProb)
        plt.title("generation: " + str(data))
        # update data
        mat.set_data(convert_matrix(dims, np.array(newGrid)))
        grid = newGrid
        return [mat]


# Returns if location (i,j) is on the borders of the forest
def is_on_border(i, j, rows, columns):
    return i == 0 or j == 0 or i == rows-1 or j == columns-1


# Returns if one or more neighbours of location (row,column)
# is on fire
def surround_by_fire(forest_snapshot, row, column):
    return forest_snapshot[row + 1][column] is False or \
           forest_snapshot[row - 1][column] is False or \
           forest_snapshot[row][column + 1] is False or \
           forest_snapshot[row][column - 1] is False


# Returns true_value or false_value if probability "p" has happened
def calculate_probability(p, true_value, false_value):
    if random.random() >= 1-p:
        return true_value
    return false_value


def iterate_over_forest(forest, rows, columns, fire_probability, lightning_probability, grow_probability):
    forestSnapshot = copy.deepcopy(forest)
    for row in range(rows):
        for column in range(columns):
            if not is_on_border(row, column, rows, columns):

                if forestSnapshot[row][column] is not True and forestSnapshot[row][column] is not False and forestSnapshot[row][column] is not None:
                    forest[row][column] = forestSnapshot[row][column] - 1
                    if forest[row][column] == 0:
                        forest[row][column] = None

                # If tree is on fire, then turns empty
                elif forestSnapshot[row][column] is False:
                    forest[row][column] = scorchedDays

                # If there isn't tree, then grow tree with growProbability
                elif forestSnapshot[row][column] is None:
                    forest[row][column] = calculate_probability(grow_probability, True, None)

                # If one or more neighbours is on fire, then start fire with fireProbability
                elif surround_by_fire(forestSnapshot, row, column):
                    forest[row][column] = calculate_probability(fire_probability, False, True)

                # If none of neighbours is on fire, then start fire with lightningProbability
                else:
                    forest[row][column] = calculate_probability(lightning_probability, False, True)
    return forest


def animation_execution(rows, columns, treeProbability, fireProbability, lightningProbability,
                 growProbability, forest):
    global dims, grid, mat
    global treeProb, fireProb, lightningProb, growProb

    treeProb, fireProb, lightningProb, growProb = (treeProbability, fireProbability,
                                                   lightningProbability, growProbability)
    dims = (rows, columns)
    grid = forest
    fig, ax = plt.subplots()
    mat = get_display_matrix(dims, ax, grid)
    anim = animation.FuncAnimation(fig, animate, frames=1000,
                                   interval=1, repeat=False)
    plt.show()
    return grid
