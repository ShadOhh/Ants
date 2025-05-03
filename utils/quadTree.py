from utils.quadTreeNode import QuadtreeNode

class Quadtree:
    def __init__(self, width, height, max_objects=4, max_levels=5):
        self.root = QuadtreeNode((0, 0, width, height), max_objects, max_levels)

    def insert(self, obj):
        self.root.insert(obj)

    def query(self, center, radius):
        return self.root.query((center[0] - radius, center[1] - radius, radius * 2, radius * 2))

    def update(self, obj):
        self.root.remove(obj)
        self.root.update_position(obj)

    def clear(self):
        self.root = QuadtreeNode(self.root.bounds, self.root.max_objects, self.root.max_levels)