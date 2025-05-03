import numpy as np

class QuadtreeNode:
    def __init__(self, bounds, max_objects=4, max_levels=5, level=0, parent=None):
        self.bounds = bounds
        self.max_objects = max_objects
        self.max_levels = max_levels
        self.level = level
        self.parent = parent
        self.objects = []
        self.children = []

    def contains(self, pos):
        x, y, w, h = self.bounds
        return x <= pos[0] < x + w and y <= pos[1] < y + h

    def subdivide(self):
        x, y, w, h = self.bounds
        hw, hh = w / 2, h / 2
        self.children = [
            QuadtreeNode((x, y, hw, hh), self.max_objects, self.max_levels, self.level + 1, self),
            QuadtreeNode((x + hw, y, hw, hh), self.max_objects, self.max_levels, self.level + 1, self),
            QuadtreeNode((x, y + hh, hw, hh), self.max_objects, self.max_levels, self.level + 1, self),
            QuadtreeNode((x + hw, y + hh, hw, hh), self.max_objects, self.max_levels, self.level + 1, self)
        ]

    def insert(self, obj):
        if self.children:
            for child in self.children:
                if child.contains(obj.pos):
                    return child.insert(obj)

        self.objects.append(obj)
        obj._quadtree_node = self

        if len(self.objects) > self.max_objects and self.level < self.max_levels:
            if not self.children:
                self.subdivide()

            for o in self.objects[:]:
                for child in self.children:
                    if child.contains(o.pos):
                        child.insert(o)
                        self.objects.remove(o)
                        break

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
        elif self.children:
            for child in self.children:
                child.remove(obj)

    def query(self, range_bounds, found=None):
        if found is None:
            found = []
        
        x, y, w, h = self.bounds
        rx, ry, rw, rh = range_bounds

        if not (x < rx + rw and x + w > rx and y < ry + rh and y + h > ry):
            return found

        for obj in self.objects:
            if (rx <= obj.pos[0] <= rx + rw) and (ry <= obj.pos[1] <= ry + rh):
                found.append(obj)

        if self.children:
            for child in self.children:
                child.query(range_bounds, found)

        return found

    def update_position(self, obj):
        node = obj._quadtree_node
        if node and node.contains(obj.pos):
            return
        
        
        while node and not node.contains(obj.pos):
            node = node.parent

        if node is None:
            node = self  

        node.insert(obj)
