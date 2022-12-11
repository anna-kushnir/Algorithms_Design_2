class GraphColoring:
    def __init__(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            self.num = int(lines[0])
            lines = lines[1:]
            self.edges = [list(map(int, line.split())) for line in lines]
    
    def get_neighbors(self, node):
        neighbors = []
        for start, end in self.edges:
            if start == node:
                neighbors.append(end)
        return neighbors

    def get_vertex_with_highest_multiplicity(self):
        max_vertex = 0
        max_count = 0
        for vertex, odd in set(self.edges):
            count = self.edges.count(vertex)
            if count > max_count:
                max_count = count
                max_vertex = vertex
        return max_vertex

    