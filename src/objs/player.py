import pygame

from ..utils.assets import Assets
from ..utils.math.vector import Vector2D
from ..utils.animation import AnimationManager
from ..utils.input import Keys

IMP = "images/player.png"

class Player:
    def __init__(self, x, y, gravity):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0.0, 0.0)
        self.manager = AnimationManager({})
        self.speed = 20.0
        self.jumpForce = gravity*1.0
        self.gravity = gravity
        self.dir = 1
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

    def update(self, dt, events):
        self.manager.update(dt)
        #update position
        self.input(events, dt)
        self.pos += (self.vel * dt)
        #TODO: collision

    def render(self, screen: pygame.Surface):
        #debut testing
        screen.blit(self.manager.get_image(), self.pos.to_int())

    def input(self, events, dt):
        #gravity
        self.vel.y += self.gravity*dt
        #jump
        if Keys.is_pressed([Keys.space, Keys.up, Keys.w], events):
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

        
