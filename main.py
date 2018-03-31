import sys
import copy
import random


# Returns if location (i,j) is on the borders of the forest
def is_on_border(i, j):
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


# Initialize forest by tree_probability
def initialize_forest(tree_probability):
    initialized_forest = [[0 for x in range(columns)] for y in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if is_on_border(row, column):
                prob_value = None
            else:
                prob_value = calculate_probability(tree_probability, True, None)
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


def question_a_initialization(forest):
    for i in range(columns):
        forest[i][1] = False

    return forest


treeProbability = float(sys.argv[1])  # d param
fireProbability = float(sys.argv[2])  # g param
lightningProbability = float(sys.argv[3])  # f param
growProbability = float(sys.argv[4])  # p param

rows, columns = 12, 12

# Each cell is None (empty) or True (tree) or False (fire)
forest = initialize_forest(treeProbability)
numOfIterations = 200

forest = question_a_initialization(forest)

for i in range(numOfIterations):
    forestSnapshot = copy.deepcopy(forest)
    for row in range(rows):
        for column in range(columns):
            if not is_on_border(row, column):

                # If tree is on fire, then turns empty
                if forestSnapshot[row][column] is False:
                    forest[row][column] = None

                # If there isn't tree, then grow tree with growProbability
                elif forestSnapshot[row][column] is None:
                    forest[row][column] = calculate_probability(growProbability, True, None)

                # If one or more neighbours is on fire, then start fire with fireProbability
                elif surround_by_fire(forestSnapshot, row, column):
                    forest[row][column] = calculate_probability(fireProbability, False, True)

                # If none of neighbours is on fire, then start fire with lightningProbability
                else:
                    forest[row][column] = calculate_probability(lightningProbability, False, True)

print_forest(forest)

