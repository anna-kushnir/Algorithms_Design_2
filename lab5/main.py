from graph import *
from algorithm import *

if __name__ == "__main__":
    path = 'file_lab5_test2.txt'
    # f = CreateGraph()
    # f.create_and_save_to_file(path)
    scout_bees = 2
    foragers = 60
    solutions = 2
    iterations = 100
    algorithm = Algorithm(path, scout_bees, foragers, solutions, iterations)
    algorithm.bee_algorithm()