import asyncio
import pygame

from ..exit_codes import *
from ..utils.input import Keys
from ..utils.assets import Assets
from ..objs.player import Player
from ..utils.math.vector import Vector2D
from ..objs.collisions import Collisions

dt = 0.0
FPS = 60

bg_color = "blue"

player = Player(0, 100, 00.0)

cam = Vector2D(0, 0)

coll = Collisions(16, "data/level_1_collisions.json", False)

def load_assets():
    player.load_assets()
    Assets.new_image("bg", "images/level_1_bg.png")



async def Level_1(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    load_assets()
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return SHUT_DOWN   #TITLE_SCREEN

        dt = clock.tick(FPS)/1000.0
        update(dt, events)
        render(screen)

        await asyncio.sleep(0)

def update(dt:float, events):
    player.update(dt, events)
    coll.update(events)

def render(screen:pygame.Surface):
    screen.fill(bg_color)
    screen.blit(Assets.get_image("bg"), (Vector2D(0, 0) - cam).to_int())
    #renders
    player.render(screen)

    coll.render(screen, cam)
    #update screen
    pygame.display.flip()
