import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

"""
Задача розфарбовування графу (100 вершин, степінь вершини не більше 20, 
але не менше 1), класичний бджолиний алгоритм (число бджіл 30 із них 
3 розвідники).
"""

class GraphColoring:
    def __init__(self, path: str):
        self.scout_bees = 3
        self.foragers = 30
        with open(path, 'r') as f:
            lines = f.readlines()
            self.num = int(lines[0])
            lines = lines[1:]
            self.edges = [list(map(int, line.split())) for line in lines]
    
    def _get_neighbors(self, vertex: int):
        neighbors = []
        for start, end in self.edges:
            if start == vertex:
                neighbors.append(end)
            if end == vertex:
                neighbors.append(start)
        return set(neighbors)

    def _get_vertex_with_highest_multiplicity(self):
        max_vertex = 0
        max_count = 0
        vertices_in_edges = [start for start, end in self.edges] + [end for start, end in self.edges]
        for vertex in set(vertices_in_edges):
            count = vertices_in_edges.count(vertex)
            if count > max_count:
                max_count = count
                max_vertex = vertex
        return max_vertex
    
    def _get_available_color(self, vertex: int, num_of_colors: int, vertex_colors: list[int]):
        neighbors = self._get_neighbors(vertex)
        available_colors = [color for color in range(num_of_colors)]
        if vertex_colors[vertex] in available_colors:
            available_colors.remove(vertex_colors[vertex])
        for neighbor in neighbors:
            if vertex_colors[neighbor] in available_colors:
                available_colors.remove(vertex_colors[neighbor])
        if len(available_colors) == 0:
            return -1
        return available_colors[0]
    
    def _is_color_available(self, vertex: int, color: int, vertex_colors: list[int]):
        neighbors = self._get_neighbors(vertex)
        for neighbor in neighbors:
            if vertex_colors[neighbor] == color:
                return False
        return True

    def greedy_algorithm(self):
        self.vertex_colors = [-1 for i in range(self.num)]
        curr_color = 0
        while -1 in self.vertex_colors:
            for vertex in range(self.num):
                if self.vertex_colors[vertex] == -1:
                    if self._is_color_available(vertex, curr_color, self.vertex_colors):
                        self.vertex_colors[vertex] = curr_color
            curr_color += 1
        self.draw_graph()
        return curr_color

    def bee_algorithm(self):
        num_of_colors = self.greedy_algorithm()
        self.draw_graph()

    def draw_graph(self):
        print('Number of colors:', len(set(self.vertex_colors)))
        print('Colors of vertices:', self.vertex_colors)
        graph = nx.Graph()
        for u, v in self.edges:
            graph.add_edge(u, v)
        pos = nx.spring_layout(graph)
        colors = ['red', 'magenta', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'brown', 'grey', 'black']
        vertex_colors_names = [colors[self.vertex_colors[vertex]] for vertex in graph.nodes()]
        nx.draw(graph, pos, with_labels = True, node_color = vertex_colors_names, edge_color = 'black', alpha = 0.7)
        plt.show()