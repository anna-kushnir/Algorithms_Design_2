from graph import *
from algorithm import *

if __name__ == "__main__":
    path = 'file_lab5_test.txt'
    # flag = str(input('Do you want to read the graph from a ready-made file or randomly generate it? (F/R)'))
    # if flag != 'F' and flag != 'f':
    #     f = CreateGraph()
    #     f.create_and_save_to_file(path)
    scout_bees = 3
    foragers = 30
    solutions = 2
    iterations = 50
    algorithm = Algorithm(path, scout_bees, foragers, solutions, iterations)
    algorithm.bee_algorithm()