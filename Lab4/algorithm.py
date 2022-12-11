class GraphColoring:
    def __init__(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            self.num = int(lines[0])
            lines = lines[1:]
            self.edges = [list(map(int, line.split())) for line in lines]