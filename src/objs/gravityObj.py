import pygame

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

    def update(self, dt, events):
        rects: list[pygame.Rect] = self.coll.get_tiles_around(self.pos)
        self.vel.y += self.gravity*dt
        #y collisions
        self.pos.y += self.vel.y * dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.y > 0: #down
                    self.pos.y -= self.vel.y * dt
                    self.vel.y = 0
                elif self.vel.y < 0: #up
                    self.vel.y = 0
                    self.pos.y = rect.bottom

    def change_gravity(self, gravity):
        self.gravity = gravity

    def rect(self):
        return pygame.Rect(self.pos.to_int(), self.image.get_size())

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.pos.to_int())

class Box(GravityObj):
    def __init__(self, x, y, gravity, collisions: Collisions, image):
        super().__init__(x, y, gravity, collisions, image)
        
