import pygame
from random import randint as ri

from src.utils.assets import Assets
from src.utils.math.vector import Vector2D
from src.utils.input import Keys
from .collisions import Collisions

class GravityObj:
    def __init__(self, x, y, gravity, collisions: Collisions, image):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0.0, 0.0)
        self.image = image
        self.gravity = gravity
        self.coll = collisions
        self.falling = False

    def update(self, dt, events):
        rects: list[pygame.Rect] = self.coll.get_tiles_around(self.pos)
        self.vel.y += self.gravity*dt
        #y collisions
        self.pos.y += self.vel.y * dt
        for rect in rects:
            if self._rect().colliderect(rect):
                self.on_floor = True
                if self.vel.y > 0: #down
                    self.pos.y -= self.vel.y * dt
                    self.vel.y = 0
                elif self.vel.y < 0: #up
                    self.vel.y = 0
                    self.pos.y = rect.bottom
        if self.vel.y != 0: self.falling = True
        else: self.falling = False

    def change_gravity(self, gravity):
        self.gravity = gravity

    def rect(self):
        if not self.falling:
            return pygame.Rect(self.pos.to_int(), self.image.get_size())
        else:
             return pygame.Rect(0, 0, 1, 1)

    def _rect(self):
         return pygame.Rect(self.pos.to_int(), self.image.get_size())

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.pos.to_int())

class Box(GravityObj):
    def __init__(self, x, y, gravity, collisions: Collisions, image):
        super().__init__(x, y, gravity, collisions, image)

class Balloon(GravityObj):
    def __init__(self, x, y, gravity, collisions: Collisions, image):
        super().__init__(x, y, -gravity, collisions, image)
        self.max = 4
        self.min = 4
        self.float = Vector2D(ri(self.min, self.max), ri(self.min, self.max))
        self.dir = Vector2D(ri(-1, 1), ri(-1, 1))

    def update(self, dt, events):
            #update float
            self.float += self.dir
            self.float.x = max(self.min, min(self.float.x, self.max))
            self.float.y = max(self.min, min(self.float.y, self.max))
            #update dir
            if ri(0, 100) == 0: self.dir.x = ri(-1, 1)
            if ri(0, 100) == 0: self.dir.y = ri(-1, 1)
            
            rects: list[pygame.Rect] = self.coll.get_tiles_around(self.pos)
            self.vel.y += self.gravity*dt
            #y collisions
            self.pos.y += self.vel.y * dt
            for rect in rects:
                if self._rect().colliderect(rect):
                    if self.vel.y > 0: #down
                        self.pos.y -= self.vel.y * dt
                        self.vel.y = 0
                    elif self.vel.y < 0: #up
                        self.vel.y = 0
                        self.pos.y = rect.bottom
        

    def change_gravity(self, gravity):
            self.gravity = -gravity

    def render(self, screen: pygame.Surface):
            screen.blit(self.image, (self.pos+self.float).to_int())
        
