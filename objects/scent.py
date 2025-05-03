from utils.vectormethods import inverse
import time
import pygame
class Scent:
    def __init__(self, pos, vector, type, screen):
        self.pos = pos
        self.vector = inverse(vector)
        self.duration = 30
        self.strength = 1
        self.type = type.lower()
        self.start_time = time.time()
        self.radius = 2
        self.screen = screen
        self._quadtree_node = None

    def update(self):
        elapsed = time.time() - self.start_time
        decay_ratio = max(0.0, 1.0 - (elapsed / self.duration))
        self.strength = decay_ratio
        # print("Scent updated")
        self.draw()
    
    def is_depleted(self):
        return self.strength <= 0.0
    
    def draw(self):
        if self.type == "home":
            pygame.draw.circle(self.screen, "blue", self.pos, self.radius)
        elif self.type == "food":
            pygame.draw.circle(self.screen, "red", self.pos, self.radius)
    
    def strengthenScent(self):
        self.strength = 1
        self.duration += 20.0
    