import pygame

from ..utils.assets import Assets
from ..utils.math.vector import Vector2D
from ..utils.animation import AnimationManager
from ..utils.input import Keys
from .collisions import Collisions

IMP = "images/player.png"


class Player:
    def __init__(self, x, y, gravity, collisions: Collisions):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0.0, 0.0)
        self.manager = AnimationManager({})
        self.speed = 20.0
        self.JFM = 0.5
        self.jumpForce = gravity*self.JFM
        self.gravity = gravity
        self.dir = 1
        self.coll = collisions

        self.on_wall = False
        self.on_floor = False
    def load_assets(self):
        # define images (swapped left/right rects)
        Assets.new_image("p_idle_left", IMP, pygame.Rect(32, 0, 32, 16))
        Assets.new_image("p_idle_right", IMP, pygame.Rect(0, 0, 32, 16))
        Assets.new_image("p_walk_left", IMP, pygame.Rect(32, 32, 32, 16))
        Assets.new_image("p_walk_right", IMP, pygame.Rect(0, 16, 32, 16))

        # defining animations
        Assets.new_animation("player_idle_left", Assets.get_image("p_idle_left"))
        Assets.new_animation("player_idle_right", Assets.get_image("p_idle_right"))
        Assets.new_animation("player_walk_left", Assets.get_image("p_walk_left"), fps=5)
        Assets.new_animation("player_walk_right", Assets.get_image("p_walk_right"), fps=5)

        # defining animation manager
        self.manager.new_anim("idle_left", Assets.get_animation("player_idle_left"))
        self.manager.new_anim("idle_right", Assets.get_animation("player_idle_right"))
        self.manager.new_anim("walk_left", Assets.get_animation("player_walk_left"))
        self.manager.new_anim("walk_right", Assets.get_animation("player_walk_right"))

        # set initial animation
        self.manager.change_anim("idle_left")

    def rect(self):
        return pygame.Rect((self.pos.x, self.pos.y), self.manager.get_image().get_size())

    def change_gravity(self, gravity):
        self.gravity = gravity
        self.jumpForce = gravity*self.JFM
        self.manager.flip_v()

    def update(self, dt, events):
        self.manager.update(dt)
        #update position
        self.input(events, dt)

        rects: list[pygame.Rect] = self.coll.get_tiles_around(self.pos)
        self.on_wall = False
        self.on_floor = False

        #x collisions
        self.pos.x += self.vel.x * dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.x > 0: #right
                    self.pos.x -= self.vel.x * dt
                    self.vel.x = 0
                    self.on_wall = True
                elif self.vel.x < 0: #left
                    self.pos.x -= self.vel.x * dt
                    self.vel.x = 0
                    self.on_wall = True
        #y collisions
        self.pos.y += self.vel.y * dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.y > 0: #down
                    self.pos.y -= self.vel.y * dt
                    self.vel.y = 0
                    self.on_floor = True
                elif self.vel.y < 0: #up
                    self.vel.y = 0
                    self.pos.y = rect.bottom
                    self.on_floor = True

    def render(self, screen: pygame.Surface):
        #debut testing
        pygame.draw.rect(screen, "red", self.rect(), 1)
        screen.blit(self.manager.get_image(), self.pos.to_int())

    def input(self, events, dt):
        #gravity
        #if not on_floor: 
        self.vel.y += self.gravity*dt
        #jump
        if Keys.is_pressed([Keys.space, Keys.up, Keys.w], events) and self.on_floor:
            self.vel.y = -self.jumpForce
        #movement
        dir = 0
        if Keys.is_held(Keys.d): dir = 1
        if Keys.is_held(Keys.a): dir = -1
        self.vel.x = dir * self.speed
        if dir!=0: self.dir = dir
        if dir == 1: self.manager.change_anim("walk_right")
        elif dir == -1: self.manager.change_anim("walk_left")
        else: self.manager.change_anim("idle_right" if self.dir > 0 else "idle_left")

        
