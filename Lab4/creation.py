import numpy as np

class CreateGraph:
    def __init__(self, num = 100, min_pow = 1, max_pow = 20):
        self.num = num
        self.min_pow = min_pow
        self.max_pow = max_pow

    def create(self, path):
        with open(path, 'w') as f:
            f.write(str(self.num) + '\n')
            for i in range(self.num):
                num_of_neighbors = np.random.randint(1, self.max_pow + 1)
                all_vertices = np.arange(self.num)
                np.random.shuffle(all_vertices)
                neighboring_vertices = all_vertices[:num_of_neighbors]
                for neighbor in neighboring_vertices:
                    f.write(str(i) + ' ' + str(neighbor) + '\n')