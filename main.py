import sys
import numpy as np
import random


def is_on_border(i, j):
    return i == 0 or j == 0 or i == rows-1 or j == columns-1


def calculate_probability(p, true_value, false_value):
    if random.random() >= 1-p:
        return true_value
    return false_value


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


treeProbability = float(sys.argv[1])
fireProbability = float(sys.argv[2])
lightningProbability = float(sys.argv[3])
growProbability = float(sys.argv[4])

rows, columns = 6, 6

forest = initialize_forest(treeProbability)
print forest
