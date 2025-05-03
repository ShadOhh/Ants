from objects.ants import Ant
from objects.food import Food
from objects.scent import Scent
from objects.colony import Colony
from utils.quadTree import Quadtree
from utils.vectorgrid import VectorGrid

class World:
    def __init__(self, screen, width, height, grid_cell_size):
        self.screen = screen
        self.worldObjects = []

        self.worldQuadtree = Quadtree(width, height)
        self.scentGrid = VectorGrid(grid_cell_size)

    def addAnt(self, pos):
        ant = Ant(pos, self.screen, self.worldQuadtree, self.scentGrid)
        self.worldObjects.append(ant)
        self.worldQuadtree.insert(ant)

    def addFood(self, pos):
        food = Food(pos, self.screen)
        self.worldObjects.append(food)
        self.worldQuadtree.insert(food)

    def addColony(self, pos):
        colony = Colony(pos, self.screen, self.worldQuadtree, self.worldObjects, self.scentGrid)
        self.worldObjects.append(colony)
        self.worldQuadtree.insert(colony)

    def addScent(self, scent, pos):
        self.scentGrid.add(scent, pos)

    def update(self):

        self.scentGrid.decay_all()
        for obj in self.worldObjects:
            if isinstance(obj, Scent):
                self.addScent(obj, obj.pos)

        for obj in self.worldObjects:
            if isinstance(obj, Food):
                if obj.is_depleted():
                    self.worldObjects.remove(obj)
                    if obj._quadtree_node:
                        obj._quadtree_node.remove(obj)
                    continue

            self.worldQuadtree.root.update_position(obj)

        self.scentGrid.draw_debug(self.screen)
        
        for obj in self.worldObjects:
            obj.update()
