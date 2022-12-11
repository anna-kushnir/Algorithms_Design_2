"""
Задача розфарбовування графу (100 вершин, степінь вершини не більше 20, 
але не менше 1), класичний бджолиний алгоритм (число бджіл 30 із них 
3 розвідники).
"""

class GraphColoring:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            lines = f.readlines()
            self.num = int(lines[0])
            lines = lines[1:]
            self.edges = [list(map(int, line.split())) for line in lines]
        self.remove_duplicate_edges()
    
    def remove_duplicate_edges(self):
        lst = []
        for start, end in self.edges:
            if start != end:
                if ([start, end] not in lst) and ([end, start] not in lst):
                    lst.append([start, end])
        self.edges = lst
    
    def get_neighbors(self, vertex: int):
        neighbors = []
        for start, end in self.edges:
            if start == vertex:
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
    
    def get_available_color(self, vertex: int, vertex_colors: list[int], num_of_colors: int):
        neighbors = self.get_neighbors(vertex)
        available_colors = [color for color in range(num_of_colors)]
        if vertex_colors[vertex] in available_colors:
            available_colors.remove(vertex_colors[vertex])
        for neighbor in neighbors:
            if vertex_colors[neighbor] in available_colors:
                available_colors.remove(vertex_colors[neighbor])
        if len(available_colors) == 0:
            return -1
        return available_colors[0]