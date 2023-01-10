import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

"""
Задача розфарбовування графу (300 вершин, степінь вершини не більше 30, 
але не менше 2), бджолиний алгоритм.
"""

class Graph:
    """
    Слугує для збереження структури графу.
    """
    def __init__(self, path: str):
        self.edges = []
        self.vertex_num = 0
        self.counts = []
        with open(path, 'r') as f:
            lines = f.readlines()
            self.vertex_num = int(lines[0])
            lines = lines[1:]
            self.edges = [list(map(int, line.split())) for line in lines]
            self._count_occurence_of_vertices_and_sort()
    
    def get_neighbors(self, vertex: int):
        """Повертає всіх сусідів заданої вершини vertex."""
        neighbors = []
        for start, end in self.edges:
            if start == vertex:
                neighbors.append(end)
            if end == vertex:
                neighbors.append(start)
        return neighbors
    
    def draw_colored_graph(self, header: str, solution: list[int]):
        """Виводить граф з даним розфарбуванням вершин."""
        if header != '':
            print(header)
            print('Number of colors:', len(set(solution)))
        graph = nx.Graph()
        for u, v in self.edges:
            graph.add_edge(u, v)
        pos = nx.spring_layout(graph)
        colors = ['red', 'magenta', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'brown', 'grey', 'black']
        vertex_colors_names = [colors[solution[vertex]] for vertex in graph.nodes()]
        nx.draw(graph, pos, with_labels = True, node_color = vertex_colors_names, edge_color = 'black', alpha = 0.7)
        plt.show()
    
    def _count_occurence_of_vertices_and_sort(self):
        """Рахує кількість зв'язків з кожною із вершин i 
        сортує створений список кількостей y порядку спадання."""
        vertices_in_edges = [edge[0] for edge in self.edges] + [edge[1] for edge in self.edges]
        self.counts = []
        for vertex in set(vertices_in_edges):
            self.counts.append([vertex, vertices_in_edges.count(vertex)])
        def func(elem: list[int]):
            return elem[1]
        self.counts.sort(key = func, reverse = True)


class Solution:
    """
    Слугує для збереження даних про конкретне рішення
    (певне розфарбування графу).
    """
    def __init__(self, graph: Graph, solution: list[int] = []):
        self.graph = graph
        self.solution = solution
        self.colors_num = self.count_colors()
        self.last_color_num = self.count_occurrences_of_last_color()
    
    def count_colors(self):
        return len(set(self.solution))
    
    def count_occurrences_of_last_color(self):
        return self.solution.count(self.colors_num)

    def greedy_algorithm(self):
        """Жадібний алгоритм розфарбування графа."""
        self.solution = [-1] * self.graph.vertex_num
        curr_color = 0
        vertices = np.arange(self.graph.vertex_num)
        np.random.shuffle(vertices)
        while -1 in self.solution:
            for vertex in vertices:
                if self.solution[vertex] == -1:
                    if self._is_color_available(vertex, curr_color):
                        self.solution[vertex] = curr_color
            curr_color += 1
        self.colors_num = self.count_colors()
        self.last_color_num = self.count_occurrences_of_last_color()

    def get_neighbor_solution(self):
        """Повертає рішення, близьке до поточного, але з деякими змінами
        та покращеннями."""
        if len(self.solution) == 0:
            return Solution(self.graph)
        vertex = np.random.randint(self.graph.vertex_num)
        neighbors = self.graph.get_neighbors(vertex)
        np.random.shuffle(neighbors)
        solution_to_return = self.solution.copy()
        for neighbor in neighbors:
            temp_solution = solution_to_return.copy()
            temp_solution[vertex], temp_solution[neighbor] = temp_solution[neighbor], temp_solution[vertex]
            new_color1 = self._get_available_color(vertex, temp_solution)
            if new_color1 != -1:
                temp_solution[vertex] = new_color1
                new_color2 = self._get_available_color(neighbor, temp_solution)
                if new_color2 != -1:
                    temp_solution[neighbor] = new_color2
                    solution_to_return = temp_solution.copy()
        return Solution(self.graph, solution_to_return)

    def _is_color_available(self, vertex: int, color: int, solution: list[int] = []):
        """Перевіряє, чи можна розмалювати дану вершину даним кольором 
        без виникнення конфліктів."""
        if solution == []:
            solution = self.solution
        neighbors = self.graph.get_neighbors(vertex)
        for neighbor in neighbors:
            if solution[neighbor] == color:
                return False
        return True

    def _get_available_color(self, vertex: int, solution: list[int] = []):
        """Шукає колір, доступний для розмалювання даної вершини."""
        if solution == []:
            solution = self.solution
        neighbors = self.graph.get_neighbors(vertex)
        available_colors = list(np.arange(len(set(solution))))
        if solution[vertex] in available_colors:
            available_colors.remove(solution[vertex])
        for neighbor in neighbors:
            if solution[neighbor] in available_colors:
                available_colors.remove(solution[neighbor])
        if len(available_colors) == 0:
            return -1
        return available_colors[0]


class Algorithm:
    """
    Слугує для ініціалізації та запуску алгоритму.
    """
    def __init__(self, path: str, scouts_num: int, foragers_num: int, solutions_num: int, iterations_num: int):
        self.scouts_num = scouts_num
        self.foragers_num = foragers_num
        self.solutions_num = solutions_num
        self.iterations_num = iterations_num
        self.probability = 0.4
        self.graph = Graph(path)
        self.solutions: list[Solution] = self._create_list_of_solutions()
        self._sort_solutions()
        self.best_solution: Solution = self.solutions[0]
    
    def _create_list_of_solutions(self):
        """Ініціалізує ділянки для розвідки та пошуку."""
        solutions: list[Solution] = []
        for i in range(self.solutions_num):
            solutions.append(Solution(self.graph))
            solutions[i].greedy_algorithm()
        return solutions

    def _sort_solutions(self):
        """Сортує рішення y порядку зростання цільової функції
        (кількості використаних кольорів)."""
        for i in range(len(self.solutions)):
            for j in range(i + 1, len(self.solutions)):
                if (self.solutions[i].colors_num > self.solutions[j].colors_num or 
                self.solutions[i].colors_num == self.solutions[j].colors_num and self.solutions[i].last_color_num > self.solutions[j].last_color_num):
                    temp = self.solutions[i]
                    self.solutions[i] = self.solutions[j]
                    self.solutions[j] = temp

    def _send_scout(self, curr_best_sltn_index: int, visited_indexes: list[int]):
        """Відправляє бджолу-розвідника на ділянку (рішення).
        Повертає True, якщо ділянку ще не відвідували інші i 
        на неї було відправлено розвідника."""
        if np.random.random_sample() > self.probability:
            if curr_best_sltn_index in visited_indexes:
                curr_best_sltn_index += 1
                return False
            visited_indexes.append(curr_best_sltn_index)
            self._send_foragers(curr_best_sltn_index)
        else:
            index = np.random.randint(self.solutions_num)
            if index in visited_indexes:
                return False
            visited_indexes.append(index)
            self._send_foragers(index)
        return True

    def _send_foragers(self, sltn_index: int):
        """Відправляє фуражирів на ділянку для дослідження її околу 
        (сусідніх ділянок)."""
        best_neighbor = self.solutions[sltn_index].get_neighbor_solution()
        for i in range(1, self.foragers_num):
            curr_neighbor = self.solutions[sltn_index].get_neighbor_solution()
            if (curr_neighbor.colors_num < best_neighbor.colors_num or
            curr_neighbor.colors_num == best_neighbor.colors_num and curr_neighbor.last_color_num <= best_neighbor.last_color_num):
                best_neighbor = curr_neighbor
        if (best_neighbor.colors_num < self.solutions[sltn_index].colors_num or
        best_neighbor.colors_num == self.solutions[sltn_index].colors_num and best_neighbor.last_color_num <= self.solutions[sltn_index].last_color_num):
            self.solutions[sltn_index] = best_neighbor
        if (self.solutions[sltn_index].colors_num < self.best_solution.colors_num or
        self.solutions[sltn_index].colors_num == self.best_solution.colors_num and self.solutions[sltn_index].last_color_num <= self.best_solution.last_color_num):
            self.best_solution = self.solutions[sltn_index]


    def bee_algorithm(self):
        """Запускає бджолиний алгоритм."""
        for i in range(self.iterations_num):
            visited_indexes = []
            curr_best_sltn_index = 0
            scouts_sent = 0
            while scouts_sent < self.scouts_num and scouts_sent < self.solutions_num:
                if self._send_scout(curr_best_sltn_index, visited_indexes):
                    scouts_sent += 1
            self._sort_solutions()
            if i == 0:
                self.graph.draw_colored_graph('', self.best_solution.solution)
            if (i + 1) % 20 == 0:
                print('Iteration: ' + str(i + 1))
                print('Best number of colors:', self.best_solution.colors_num)
                # self.graph.draw_colored_graph('', self.best_solution.solution)
        self.graph.draw_colored_graph('THE RESULT OF BEES ALGORITHM', self.best_solution.solution)
        return self.best_solution
