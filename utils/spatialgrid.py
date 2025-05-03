class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def clear(self):
        self.cells.clear()

    def add(self, obj, pos):
        key = (int(pos[0] // self.cell_size), int(pos[1] // self.cell_size))
        if key not in self.cells:
            self.cells[key] = []
        self.cells[key].append(obj)

    def printAll(self):
        return self.cells

    def query(self, pos, radius):
        cx, cy = int(pos[0] // self.cell_size), int(pos[1] // self.cell_size)
        r = int(radius // self.cell_size) + 1

        nearby = []
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                key = (cx + dx, cy + dy)
                if key in self.cells:
                    nearby.extend(self.cells[key])
        return nearby
