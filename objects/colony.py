
import pygame

class Colony():
    def __init__(self, pos, screen, worldGrid, worldObjects, scentGrid, worldScent):
        self.worldObjects = worldObjects
        
        self.scentGrid = scentGrid
        self.worldScent = worldScent
        self.worldGrid = worldGrid
        self.pos = pos
        self.screen = screen
        self.radius = 40
        self.storage = 200
        self.spawnReq = 10
        self._quadtree_node = None

    def draw(self):
        pygame.draw.circle(self.screen, "Gray", self.pos, self.radius)
    
    def deposit(self, amt):
        self.storage += amt

    def update(self):
        # print("Colony Updated")
        self.spawnAnt()
        self.draw()
    
    def spawnAnt(self):
        if self.storage >= self.spawnReq:
            self.storage -= self.spawnReq
            from objects.ants import Ant
            self.worldObjects.append(Ant(self.pos, self.screen, self.worldGrid, self.scentGrid, self.worldScent))
            print("SpawnCalled")