import asyncio
import pygame

from ..exit_codes import *
from ..utils.input import Keys
from ..utils.assets import Assets
from ..objs.player import Player

dt = 0.0
FPS = 60

bg_color = "blue"

player = Player(0, 0, 30.0)

def load_assets():
    player.load_assets()



async def Level_1(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    load_assets()
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return TITLE_SCREEN

        dt = clock.tick(FPS)/1000.0
        update(dt, events)
        render(screen)

        await asyncio.sleep(0)

def update(dt:float, events):
    player.update(dt, events)

def render(screen:pygame.Surface):
    screen.fill(bg_color)
    #renders
    player.render(screen)
    #update screen
    pygame.display.flip()
