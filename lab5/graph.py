import numpy as np

class CreateGraph:
    def __init__(self, num: int = 300, min_pow: int = 2, max_pow: int = 30):
        self.num = num
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.edges = []

    def create_and_save_to_file(self, path: str):
        self._generate_graph()
        with open(path, 'w') as f:
            f.write(str(self.num) + '\n')
            for edge in self.edges:
                f.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
    
    def _generate_graph(self):
        counts = [0 for i in range(self.num)]
        for vertex in range(self.num):
            num_of_neighbors = np.random.randint(self.min_pow, self.max_pow)
            if counts[vertex] + num_of_neighbors > self.max_pow:
                num_of_neighbors = self.max_pow - counts[vertex]
            counts[vertex] += num_of_neighbors
            i = 0
            neighbors = []
            while i < num_of_neighbors:
                neighbor = np.random.randint(0, self.num)
                if vertex != neighbor and ([vertex, neighbor] not in self.edges) and ([neighbor, vertex] not in self.edges):
                    if counts[neighbor] < self.max_pow:
                        neighbors.append(neighbor)
                        counts[neighbor] += 1
                        i += 1
            for neighbor in neighbors:
                self.edges.append([vertex, neighbor])