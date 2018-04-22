import sys
import itertools
import numpy
from numpy import *
import matrix
import matplotlib.pyplot as plt


# Initialize forest by tree_probability
def initialize_forest():
    initialized_forest = [[0 for x in range(columns)] for y in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if matrix.is_on_border(row, column, rows, columns):
                prob_value = None
            else:
                prob_value = matrix.calculate_probability(treeProbability, True, None)
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


# count number of empty cells and tree cells - for index
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
    two_thirds_of_local_forest = (10 * 10) * 2 / 3
    for i in range(rows / 10):
        for j in range(columns / 10):
            # get index for local part of forest
            numbers = get_number_of_trees_and_empty(array(forest)[10 * i:10 * (i + 1), 10 * j:10 * (j + 1)])
            if numbers["trees"] > two_thirds_of_local_forest or \
                    numbers["empties"] > two_thirds_of_local_forest:
                fields_with_majority += 1
    return fields_with_majority


# perform x life cycles (200 generations) of simulation
def iterate_x_times_over_forest(initialization_func, lightning_prob, grow_prob, fire_prob, num_of_iterations):
    global_index_sum = 0
    x_data = []
    y1_data = []
    y2_data = []

    for i in range(num_of_iterations):
        forest = initialization_func()
        for j in range(200):  # 1 life cycle
            forest = matrix.iterate_over_forest(forest, rows, columns, fire_prob,
                                                lightning_prob, grow_prob) # update forest board
            x_data.append(j)
            y1_data.append(get_global_index(forest))
            y2_data.append(get_local_index(forest))

        global_index_sum += get_global_index(forest)

    if question == "d":  # show graph of local and global indices
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x_data, y1_data, 'b-', label="global index")
        ax.tick_params('y', colors="blue")
        ax2 = ax.twinx()
        ax2.plot(x_data, y2_data, 'r-', label="local fields")
        ax2.tick_params('y', colors="red")
        fig.tight_layout()

    return float(global_index_sum) / num_of_iterations


# *********************** QUESTION A ****************************
def question_a_initialization():
    init_forest = initialize_forest()
    for i in range(columns):
        init_forest[i][1] = False
    init_forest[0][1] = None
    init_forest[rows - 1][1] = None

    return init_forest


def simulate_question_a():
    global treeProbability, lightningProbability, growProbability
    treeProbability = 1
    lightningProbability = 0
    growProbability = 0

    current_fire_prob = 0
    last_prob_with_positive_global_index = 0
    first_prob_with_negative_global_index = 0.01
    x_data = []
    y_data = []

    while current_fire_prob <= 1:  # get global index for all fire probabilities between 0 to 1
        average_global_index = iterate_x_times_over_forest(question_a_initialization,
                                                           lightningProbability,
                                                           growProbability,
                                                           current_fire_prob,
                                                           3)

        if average_global_index > 1:
            last_prob_with_positive_global_index = current_fire_prob + 0.001
            first_prob_with_negative_global_index = last_prob_with_positive_global_index + 0.01

        x_data.append(current_fire_prob)
        y_data.append(average_global_index)
        current_fire_prob += 0.01

    while last_prob_with_positive_global_index < first_prob_with_negative_global_index:
        # get more accurate values near critical point
        average_global_index = iterate_x_times_over_forest(question_a_initialization,
                                                           lightningProbability,
                                                           growProbability,
                                                           last_prob_with_positive_global_index,
                                                           3)
        x_data.append(last_prob_with_positive_global_index)
        y_data.append(average_global_index)
        print last_prob_with_positive_global_index, average_global_index
        last_prob_with_positive_global_index += 0.001

        lists = sorted(itertools.izip(*[x_data, y_data]))
        x_data, y_data = list(itertools.izip(*lists))
        plt.plot(x_data, y_data)
        plt.show()


# *********************** QUESTION B ***************************

def question_b_check_fire_probability():
    global lightningProbability, growProbability, fireProbability

    x_data = []
    y_data = []

    lightningProbability, growProbability = 0.5, 0.5
    fireProbability = 0
    while fireProbability <= 1:
        average_global_index = iterate_x_times_over_forest(initialize_forest,
                                                           lightningProbability,
                                                           growProbability,
                                                           fireProbability,
                                                           3)
        x_data.append(fireProbability)
        y_data.append(average_global_index)
        fireProbability += 0.1
    fig_fire = plt.figure()
    ax = fig_fire.add_subplot(111)
    ax.plot(x_data, y_data)
    plt.xlabel("fire probability")


def question_b_check_grow_probability():
    global lightningProbability, growProbability, fireProbability

    x_data = []
    y_data = []

    lightningProbability, fireProbability = 0.5, 0.5
    growProbability = 0
    while growProbability <= 1:
        average_global_index = iterate_x_times_over_forest(initialize_forest,
                                                           lightningProbability,
                                                           growProbability,
                                                           fireProbability,
                                                           3)
        x_data.append(growProbability)
        y_data.append(average_global_index)
        growProbability += 0.1
    fig_grow = plt.figure()
    ax = fig_grow.add_subplot(111)
    ax.plot(x_data, y_data)
    plt.xlabel("grow probability")


def question_b_check_lightning_probability():
    global lightningProbability, growProbability, fireProbability

    x_data = []
    y_data = []
    growProbability, fireProbability = 0.5, 0.5
    lightningProbability = 0
    while lightningProbability <= 1:
        average_global_index = iterate_x_times_over_forest(initialize_forest,
                                                           lightningProbability,
                                                           growProbability,
                                                           fireProbability,
                                                           3)
        x_data.append(lightningProbability)
        y_data.append(average_global_index)
        lightningProbability += 0.1
    fig_lightning = plt.figure()
    ax = fig_lightning.add_subplot(111)
    ax.plot(x_data, y_data)
    plt.xlabel("lightning probability")


def simulate_question_b():
    global treeProbability
    treeProbability = 0.5

    question_b_check_fire_probability()
    question_b_check_grow_probability()
    question_b_check_lightning_probability()


# *********************** QUESTION D ***************************

def simulate_question_d():
    iterate_x_times_over_forest(initialize_forest, lightningProbability,
                                growProbability, fireProbability, 1)


treeProbability = float(sys.argv[1])  # d param
fireProbability = float(sys.argv[2])  # g param
lightningProbability = float(sys.argv[3])  # f param
growProbability = float(sys.argv[4])  # p param

question = None
if len(sys.argv) == 6:
    question = sys.argv[5]

rows, columns = 100, 100

# Each cell is None (empty) or True (tree) or False (on fire)
forest = initialize_forest()


if question == "a":
    simulate_question_a()

if question == "b":
    simulate_question_b()

if question == "d":
    simulate_question_d()

# show graphic board of simulation
newForest = matrix.animation_execution(rows, columns, treeProbability, fireProbability, lightningProbability,
                                       growProbability, forest)

global_index = get_global_index(newForest)
local_index = get_local_index(newForest)
print global_index, local_index
