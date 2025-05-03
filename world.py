from objects.ants import Ant
from objects.food import Food
from objects.scent import Scent
from objects.colony import Colony
from utils.quadTree import Quadtree

class World:
    def __init__(self, screen, width=800, height=600):
        self.screen = screen
        self.worldObjects = []
        self.worldScent = []

        self.worldQuadtree = Quadtree(width, height)
        self.scentQuadtree = Quadtree(width, height)

    def addAnt(self, pos):
        ant = Ant(pos, self.screen, self.worldQuadtree, self.scentQuadtree, self.worldScent)
        self.worldObjects.append(ant)
        self.worldQuadtree.insert(ant)

    def addFood(self, pos):
        food = Food(pos, self.screen)
        self.worldObjects.append(food)
        self.worldQuadtree.insert(food)

    def addColony(self, pos):
        colony = Colony(pos, self.screen, self.worldQuadtree, self.worldObjects, self.scentQuadtree, self.worldScent)
        self.worldObjects.append(colony)
        self.worldQuadtree.insert(colony)

    def update(self):
        for scent in self.worldScent:
            if scent.is_depleted():
                self.worldScent.remove(scent)
                if scent._quadtree_node:
                    scent._quadtree_node.remove(scent)
            else:
                self.scentQuadtree.root.update_position(scent)

        for obj in self.worldObjects:
            if isinstance(obj, Food):
                if obj.is_depleted():
                    self.worldObjects.remove(obj)
                    if obj._quadtree_node:
                        obj._quadtree_node.remove(obj)
                    continue

            self.worldQuadtree.root.update_position(obj)

        for obj in self.worldObjects:
            obj.update()

        for scent in self.worldScent:
            scent.update()
