import pygame
import numpy as np
from objects.scent import Scent

class VectorGridNode:
    def __init__(self, decay_rate=0.999):
        self.homevector = np.zeros(2)
        self.foodvector = np.zeros(2)
        self.decay_rate = decay_rate  # e.g., 0.99 means ~1% decay per frame

    def add(self, scent):
        # Add vector scaled by scent strength (magnitude matters)
        if scent.type == "food":
            self.foodvector += normalize(scent.vector) * scent.strength
        elif scent.type == "home":
            self.homevector += normalize(scent.vector) * scent.strength

    def decay(self):
        # Reduce magnitude, not just scale components
        home_mag = np.linalg.norm(self.homevector)
        food_mag = np.linalg.norm(self.foodvector)

        self.homevector = (
            normalize(self.homevector) * home_mag * self.decay_rate if home_mag > 0 else self.homevector
        )
        self.foodvector = (
            normalize(self.foodvector) * food_mag * self.decay_rate if food_mag > 0 else self.foodvector
        )

    def gethomeVector(self):
        return self.homevector

    def getfoodVector(self):
        return self.foodvector


class VectorGrid:
    def __init__(self, cell_size, decay_rate=0.999):
        self.cell_size = cell_size
        self.cells = {}
        self.decay_rate = decay_rate

    def clear(self):
        self.cells.clear()

    def _get_key(self, pos):
        return (int(pos[0] // self.cell_size), int(pos[1] // self.cell_size))

    def add(self, scent, pos):
        key = self._get_key(pos)
        if key not in self.cells:
            self.cells[key] = VectorGridNode(self.decay_rate)
        self.cells[key].add(scent)

    def decay_all(self):
        for node in self.cells.values():
            node.decay()

    def query(self, pos):
        key = self._get_key(pos)
        return self.cells.get(key, None)

    def printAll(self):
        return self.cells

    def draw_debug(self, screen):
        for (cx, cy), node in self.cells.items():
            center_x = cx * self.cell_size + self.cell_size / 2
            center_y = cy * self.cell_size + self.cell_size / 2
            center = np.array([center_x, center_y])

            # Draw home vector (red), scale by magnitude
            home_end = center + normalize(node.gethomeVector()) * np.linalg.norm(node.gethomeVector()) * 2
            pygame.draw.line(screen, (255, 0, 0), center, home_end, 2)
            self._draw_arrow_head(screen, center, home_end, (255, 0, 0))

            # Draw food vector (green), scale by magnitude
            food_end = center + normalize(node.getfoodVector()) * np.linalg.norm(node.getfoodVector()) * 2
            pygame.draw.line(screen, (0, 255, 0), center, food_end, 2)
            self._draw_arrow_head(screen, center, food_end, (0, 255, 0))

    def _draw_arrow_head(self, screen, start, end, color, size=5):
        direction = end - start
        if np.linalg.norm(direction) == 0:
            return
        direction = direction / np.linalg.norm(direction)

        left = np.array([-direction[1], direction[0]])
        right = np.array([direction[1], -direction[0]])

        point1 = end
        point2 = end - direction * size + left * size * 0.5
        point3 = end - direction * size + right * size * 0.5

        pygame.draw.polygon(screen, color, [point1, point2, point3])


# Helper function (if not already imported)
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v
