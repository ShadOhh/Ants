import pygame
import numpy as np
from utils.vectormethods import clamp_magnitude
from utils.vectormethods import normalize
from utils.vectormethods import facingDirection
from utils.vectormethods import angle_between
from utils.vectormethods import distance
from objects.scent import Scent
import time

import random

class Ant:
    def __init__(self, pos, screen, worldGrid, scentGrid):
        self.image = pygame.image.load("images\\image.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.pos = np.array(pos, dtype='float64')
        self.screen = screen

        # Grid references
        self.worldGrid = worldGrid
        self.scentGrid = scentGrid

        # params
        self.maxspeed = 1.0
        self.wanderStr = 0.1
        self.steerStr = 3
        self.vel = np.zeros(2)
        self.des = np.zeros(2)
        self.viewAng = 150
        self.radius = 5
        self.sightDistance = 50
        self.separationDistance = 5
        self._quadtree_node = None

        # inventory
        self.hand = 0
        self.max = 1

        # targets
        self.foodTarget = None
        self.colonyTarget = None

        # internal clock
        self.initTime = time.time()
        self.dropFreq = 0.5

        self.ANT_FONT = pygame.font.SysFont(None, 18)

    def wander(self):
        random_offset = np.random.uniform(-1, 1, 2) * self.wanderStr
        self.des = self.vel + random_offset

        norm = np.linalg.norm(self.des)
        if norm != 0:
            desired_velocity = (self.des / norm) * self.maxspeed
        else:
            desired_velocity = np.zeros(2)

        steering_force = desired_velocity - self.vel
        acceleration = clamp_magnitude(steering_force, self.steerStr)

        self.vel += acceleration
        self.vel = clamp_magnitude(self.vel, self.maxspeed)

    def draw(self):
        # Draws and Rotate the Image

        if np.linalg.norm(self.vel) != 0:
            angle = np.degrees(np.arctan2(-self.vel[1], self.vel[0])) - 90
        else:
            angle = 0 

        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.pos)
        self.screen.blit(rotated_image, rotated_rect.topleft)

        # Uncomment for debug
        self.debug()

    def debug(self):
        pygame.draw.circle(self.screen,"red",self.pos, self.radius)
        pygame.draw.circle(self.screen, "black", self.pos, self.sightDistance, width=1)
        text_surface = self.ANT_FONT.render(str(self.hand), True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.pos[0], self.pos[1] - self.radius - 8))
        self.screen.blit(text_surface, text_rect)


    def getNearby(self, distance, grid):
        nearby = grid.query(self.pos, distance)
        return nearby
    def getNearbyNode(self):
        return self.scentGrid.query(self.pos)

    # def dropScent(self):
        
    #     current_time = time.time()
        
    #     if current_time - self.initTime >= self.dropFreq:
            
    #         self.initTime = current_time
    #         if self.hand >= self.max:
    #             self.worldObjects.append(Scent(self.pos.copy(), facingDirection(self.vel), "food", self.screen))
    #         elif self.hand < self.max:
    #             self.worldObjects.append(Scent(self.pos.copy(), facingDirection(self.vel), "home", self.screen))
    #     pass

    # def dropScent(self):
    #     current_time = time.time()

    #     if current_time - self.initTime >= self.dropFreq:
    #         self.initTime = current_time

    #         scent_type = "food" if self.hand >= self.max else "home"
    #         nearby = self.getNearby(self.sightDistance, self.scentGrid)

    #         found_existing = False

    #         for obj in nearby:
    #             if isinstance(obj, Scent) and obj.type == scent_type:
    #                 if np.linalg.norm(obj.pos - self.pos) < self.sightDistance/ 2:
    #                     obj.strengthenScent()
    #                     found_existing = True
    #                     break

    #         if not found_existing:
    #             self.worldScent.append(Scent(self.pos.copy(), facingDirection(self.vel), scent_type, self.screen))

    def dropScent(self):
        current_time = time.time()

        if current_time - self.initTime >= self.dropFreq:
            self.initTime = current_time

            scent_type = "food" if self.hand >= self.max else "home"
            scent_vector = facingDirection(self.vel)

            # Add directly to the VectorGrid
            from objects.scent import Scent  # assuming you still need the type definition
            scent = Scent(self.pos.copy(), scent_vector, scent_type, self.screen)
            self.scentGrid.add(scent, self.pos)

    def trackScent(self):
        node = self.getNearbyNode()
        if node is None:
            return None

        if self.hand >= self.max:
            target_vector = node.gethomeVector()
        else:
            target_vector = node.getfoodVector()

        if np.linalg.norm(target_vector) > 0:
            return normalize(target_vector)
        return None

    def rotate180(self):
        if np.linalg.norm(self.vel) != 0:
            self.vel = -self.vel
        else:
            self.vel = -facingDirection(self.vel) * self.maxspeed * 0.1
    
    def avoidEdges(self, screen_width, screen_height, margin=20, edge_strength=0.5):
        steer = np.zeros(2)

        if self.pos[0] < margin:
            steer[0] = edge_strength
        elif self.pos[0] > screen_width - margin:
            steer[0] = -edge_strength

        if self.pos[1] < margin:
            steer[1] = edge_strength
        elif self.pos[1] > screen_height - margin:
            steer[1] = -edge_strength

        if np.linalg.norm(steer) > 0:
            steer = normalize(steer) * self.maxspeed
            steer -= self.vel
            steer = clamp_magnitude(steer, self.steerStr)

        return steer




    # def trackScent(self):
    #     nearby = self.getNearby(self.sightDistance, self.scentGrid)
    #     if self.hand >= self.max:
    #         #filter for home scent
    #         filterScent = [obj for obj in nearby if isinstance(obj, Scent) and obj.type == "home"]
    #     elif self.hand < self.max:
    #         #filter for food scent
    #         filterScent = [obj for obj in nearby if isinstance(obj, Scent) and obj.type == "food"]

    #     avgScentDirection = np.zeros(2)
    #     scent_ct = 0

    #     if len(filterScent) >= 1:
    #         for scent in filterScent:
    #             direction = normalize(scent.pos - self.pos)
    #             forward = facingDirection(self.vel)
    #             if angle_between(forward, direction) < self.viewAng / 2:
    #                 avgScentDirection += scent.vector
    #                 scent_ct += 1

    #     if np.linalg.norm(avgScentDirection) != 0:
    #         avgScentDirection /= scent_ct
    #         avgScentDirection = normalize(avgScentDirection)
    #         return avgScentDirection
        

    #     return None


    # def trackScent(self):
    #     nearby = self.getNearby(self.sightDistance, self.scentGrid)

    #     if self.hand >= self.max:
    #         # looking for home scent
    #         filterScent = [obj for obj in nearby if isinstance(obj, Scent) and obj.type == "home"]
    #     else:
    #         # looking for food scent
    #         filterScent = [obj for obj in nearby if isinstance(obj, Scent) and obj.type == "food"]

    #     combined_direction = np.zeros(2)
    #     total_weight = 0

    #     forward = facingDirection(self.vel)

    #     for scent in filterScent:
    #         direction = normalize(scent.pos - self.pos)
    #         if angle_between(forward, direction) < self.viewAng / 2:
    #             weight = scent.strength + 0.1  # slight bias for stronger scents
    #             combined_direction += normalize(scent.vector) * weight
    #             total_weight += weight

    #     if total_weight > 0:
    #         averaged_direction = combined_direction / total_weight
    #         return normalize(averaged_direction)

    #     return None
    
    # def trackScent(self):
    #     nearby = self.getNearby(self.sightDistance, self.scentGrid)
    #     if self.hand >= self.max:
    #         filterScent = [obj for obj in nearby if obj.type == "home"]
    #     else:
    #         filterScent = [obj for obj in nearby if obj.type == "food"]

    #     best_scent = None
    #     best_score = float('-inf')
    #     forward = facingDirection(self.vel)

    #     for scent in filterScent:
    #         direction = normalize(scent.pos - self.pos)
    #         alignment = np.dot(forward, direction) 
    #         if angle_between(forward, direction) < self.viewAng / 2:
                
    #             score = scent.strength * max(alignment, 0)
    #             if score > best_score:
    #                 best_scent = scent
    #                 best_score = score

    #     if best_scent:
            
    #         scent_dir = normalize(best_scent.vector)
    #         blend_factor = 0.3
    #         smooth_direction = normalize((1 - blend_factor) * self.vel + blend_factor * scent_dir)
    #         return smooth_direction

    #     return None

    # def trackScent(self):
    #     nearby = self.getNearby(self.sightDistance, self.scentGrid)
    #     if self.hand >= self.max:
    #         target_type = "home"
    #     else:
    #         target_type = "food"

    #     forward = facingDirection(self.vel)
    #     left_value = 0
    #     center_value = 0
    #     right_value = 0

    #     for scent in nearby:
    #         if not isinstance(scent, Scent) or scent.type != target_type:
    #             continue

    #         direction = normalize(scent.pos - self.pos)
    #         angle = angle_between(forward, direction)
    #         cross = np.cross(forward, direction)

    #         # Check if within field of view
    #         if angle < self.viewAng / 2:
    #             # Assign to left, center, or right
    #             if angle < self.viewAng / 6:
    #                 center_value += scent.strength
    #             elif cross > 0:
    #                 left_value += scent.strength
    #             else:
    #                 right_value += scent.strength

    #     # Decide direction
    #     if center_value > max(left_value, right_value):
    #         desired_direction = forward
    #     elif left_value > right_value:
    #         desired_direction = np.array([-forward[1], forward[0]])  # rotate left 90°
    #     else:
    #         desired_direction = np.array([forward[1], -forward[0]])  # rotate right 90°

    #     if left_value == 0 and center_value == 0 and right_value == 0:
    #         return None  # no scent, no steering

    #     return normalize(desired_direction)
        


    # Pass by reference so what i add here can be sent back to world this will be helpful for scent.

    def handleFood(self):
        from objects.food import Food
        
        if self.foodTarget == None and self.hand <= self.max:
            nearby = self.getNearby(self.sightDistance, self.worldGrid)

            filterFood = [obj for obj in nearby if isinstance(obj, Food)]

            if len(filterFood) >= 1:
                for food in filterFood:
                    direction = normalize(food.pos - self.pos)
                    forward = facingDirection(self.vel)

                    if angle_between(forward, direction) < self.viewAng / 2:
                        self.foodTarget = food
                        break
        elif self.foodTarget is not None:
            if distance(self.pos, self.foodTarget.pos) < (self.radius + self.foodTarget.radius):
                self.hand += self.foodTarget.take(self.max)
                self.foodTarget = None
                self.rotate180()


    def handleColony(self):
        from objects.colony import Colony
        
        if self.colonyTarget == None and self.hand >= self.max:
            nearby = self.getNearby(self.sightDistance, self.worldGrid)

            filterColony = [obj for obj in nearby if isinstance(obj, Colony)]

            if len(filterColony) >= 1:
                for colony in filterColony:
                    direction = normalize(colony.pos - self.pos)
                    forward = facingDirection(self.vel)

                    if angle_between(forward, direction) < self.viewAng / 2:
                        self.colonyTarget = colony
                        break
        elif self.colonyTarget is not None:
            if distance(self.pos, self.colonyTarget.pos) < (self.radius + self.colonyTarget.radius):
                self.colonyTarget.deposit(self.hand)
                self.hand = 0
                self.colonyTarget = None
                self.rotate180()


    def seek(self, target_pos):
        desired_direction = normalize(target_pos - self.pos)

        
        if np.linalg.norm(self.vel) != 0:
            forward = normalize(self.vel)
        else:
            forward = desired_direction 

        
        angle_between_vecs = np.arccos(np.clip(np.dot(forward, desired_direction), -1.0, 1.0))
        max_rotation = np.radians(self.steerStr)

        
        if angle_between_vecs < max_rotation:
            new_direction = desired_direction
        else:
            
            axis = np.cross(forward, desired_direction)
            sign = np.sign(axis) if axis != 0 else 1

            rotation_matrix = np.array([
                [np.cos(max_rotation), -sign * np.sin(max_rotation)],
                [sign * np.sin(max_rotation), np.cos(max_rotation)]
            ])
            new_direction = np.dot(rotation_matrix, forward)

        self.des = new_direction * self.maxspeed

        steering_force = self.des - self.vel
        acceleration = clamp_magnitude(steering_force, self.steerStr)

        self.vel += acceleration
        self.vel = clamp_magnitude(self.vel, self.maxspeed)


    # def separation(self):
    #     nearby = self.getNearby(self.sightDistance / 2, self.worldGrid)
    #     filterAnts = [obj for obj in nearby if isinstance(obj, Ant)]

    #     steer = np.zeros(2)
    #     count = 0

    #     for other in filterAnts:
    #         if other is self:
    #             continue

    #         dist = distance(self.pos, other.pos)
    #         if dist < self.separationDistance and dist > 0:
    #             diff = self.pos - other.pos
    #             diff = normalize(diff)
    #             # Scale the push by proximity (closer = stronger push)
    #             force_scale = ((self.separationDistance - dist) / self.separationDistance) / 10
    #             diff *= force_scale
    #             steer += diff
    #             count += 1

    #     if count > 0:
    #         steer /= count

    #     if np.linalg.norm(steer) > 0:
    #         steer = normalize(steer) * self.maxspeed
    #         steer -= self.vel
    #         steer = clamp_magnitude(steer, self.steerStr)

    #     # Apply a softening weight to prevent overpowering
    #     separation_weight = 0.1 
    #     steer *= separation_weight

    #     return steer


    # def update(self):
    #     if self.hand >= self.max:
    #         self.handleColony()
    #     elif self.hand < self.max:
    #         self.handleFood()

    #     self.dropScent()
    #     # mouse_pos = pygame.mouse.get_pos()
    #     scent_direction = self.trackScent()

    #     if self.foodTarget is not None:
    #         self.seek(self.foodTarget.pos)
    #     elif self.colonyTarget is not None:
    #         self.seek(self.colonyTarget.pos)
    #     elif scent_direction is not None:
    #         target_pos = self.pos + scent_direction * self.sightDistance
    #         self.seek(target_pos)
    #     # elif distance(self.pos, mouse_pos) < self.sightDistance:
    #     #     self.seek(mouse_pos)
    #     else:
    #         self.wander()

    #     # sep_force = self.separation()
    #     # self.vel += sep_force
    #     # self.vel = clamp_magnitude(self.vel, self.maxspeed)

    #     edge_force = self.avoidEdges(self.screen.get_width(), self.screen.get_height())
    #     self.vel += edge_force
    #     self.vel = clamp_magnitude(self.vel, self.maxspeed)

    #     self.pos += self.vel
    #     self.draw()

    def update(self):
        if self.hand >= self.max:
            self.handleColony()
        elif self.hand < self.max:
            self.handleFood()

        self.dropScent()
        scent_direction = self.trackScent()

        if self.foodTarget is not None:
            self.seek(self.foodTarget.pos)
        elif self.colonyTarget is not None:
            self.seek(self.colonyTarget.pos)
        elif scent_direction is not None:
            target_pos = self.pos + scent_direction * self.sightDistance
            self.seek(target_pos)
        else:
            self.wander()

        edge_force = self.avoidEdges(self.screen.get_width(), self.screen.get_height())
        self.vel += edge_force
        self.vel = clamp_magnitude(self.vel, self.maxspeed)

        self.pos += self.vel
        self.draw()