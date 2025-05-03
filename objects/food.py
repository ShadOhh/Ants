import random
import pygame

class Food():
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen
        self.value = random.uniform(20, 30)
        self.radius = self.value
        self._quadtree_node = None

    def is_depleted(self):
        return self.value <= 0

    def draw(self):
        self.radius = self.value
        pygame.draw.circle(self.screen, "green", self.pos, self.radius)
    
    def take(self, take):
        actual_taken = min(self.value, take)
        self.value -= actual_taken
        return actual_taken
    
    def update(self):
        
        self.draw()

