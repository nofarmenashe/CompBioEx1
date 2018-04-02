import sys
import itertools
import numpy
from numpy import *
import matrix
import matplotlib.pyplot as plt

# Initialize forest by tree_probability
def initialize_forest(tree_probability):
    initialized_forest = [[0 for x in range(columns)] for y in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if matrix.is_on_border(row, column, rows, columns):
                prob_value = None
            else:
                prob_value = matrix.calculate_probability(tree_probability, True, None)
            initialized_forest[row][column] = prob_value

    return initialized_forest


# Print forest in matrix format
def print_forest(forest):
    printedForest = [[0 for x in range(columns)] for y in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if forest[row][column] is True:
                printedForest[row][column] = "T"
            elif forest[row][column] is False:
                printedForest[row][column] = "F"
            else:
                printedForest[row][column] = "0"

    for row in printedForest:
        for val in row:
            print val,
        print


def get_number_of_trees_and_empty(forest):
    number_of_trees = 0
    number_of_empty_cells = 0
    for i in range(len(forest)):
        for j in range(len(forest[0])):
            if forest[i][j]:
                number_of_trees += 1
            if forest[i][j] is None:
                number_of_empty_cells += 1
    return {"trees": number_of_trees, "empties": number_of_empty_cells}


def get_global_index(forest):
    numbers = get_number_of_trees_and_empty(forest)
    return float(numbers["trees"]) / numbers["empties"]


def get_local_index(forest):
    fields_with_majority = 0
    two_thirds_of_local_forest = (10*10)*2/3
    for i in range(rows/10):
        for j in range(columns/10):
            numbers = get_number_of_trees_and_empty(array(forest)[10*i:10*(i+1), 10*j:10*(j+1)])
            if numbers["trees"] > two_thirds_of_local_forest or \
                    numbers["empties"] > two_thirds_of_local_forest:
                fields_with_majority += 1
    return fields_with_majority


def question_a_initialization(forest):
    for i in range(columns):
        forest[i][1] = False
    forest[0][1] = None
    forest[rows - 1][1] = None

    return forest


def iterate_x_times_over_forest(fire_prob, num_of_iterations):
    global_index_sum = 0

    for i in range(num_of_iterations):
        forest = initialize_forest(treeProbability)
        forest = question_a_initialization(forest)

        for i in range(200):
            forest = matrix.iterate_over_forest(forest, rows, columns, fire_prob,
                                                lightningProbability, growProbability)

        global_index_sum += get_global_index(forest)

    return float(global_index_sum) / num_of_iterations


def update_line(hl, new_data_x, new_data_y):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data_x))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data_y))


def simulate_question_a(forest):
    current_fire_prob = 0
    critical_point = (0, 0)
    last_prob_with_positive_global_index = 0
    first_prob_with_negative_global_index = 0.01
    x_data = []
    y_data = []

    while current_fire_prob <= 1:
        average_global_index = iterate_x_times_over_forest(current_fire_prob, 10)

        if average_global_index > 1:
            last_prob_with_positive_global_index = current_fire_prob + 0.001
            first_prob_with_negative_global_index = last_prob_with_positive_global_index + 0.01

        x_data.append(current_fire_prob)
        y_data.append(average_global_index)
        current_fire_prob += 0.1

    while last_prob_with_positive_global_index < first_prob_with_negative_global_index:
        average_global_index = iterate_x_times_over_forest(last_prob_with_positive_global_index, 10)
        x_data.append(last_prob_with_positive_global_index)
        y_data.append(average_global_index)
        last_prob_with_positive_global_index += 0.001

        lists = sorted(itertools.izip(*[x_data, y_data]))
        x_data, y_data = list(itertools.izip(*lists))
        plt.plot(x_data, y_data)
        plt.show()




treeProbability = float(sys.argv[1])  # d param
fireProbability = float(sys.argv[2])  # g param
lightningProbability = float(sys.argv[3])  # f param
growProbability = float(sys.argv[4])  # p param

question = None
if len(sys.argv) == 6:
    question = sys.argv[5]

rows, columns = 100, 100

# Each cell is None (empty) or True (tree) or False (on fire)
forest = initialize_forest(treeProbability)

if question == "a":
    simulate_question_a(forest)

newForest = matrix.animation_execution(rows, columns, treeProbability, fireProbability, lightningProbability,
                 growProbability, forest)

global_index = get_global_index(newForest)
local_index = get_local_index(newForest)
print global_index, local_index
