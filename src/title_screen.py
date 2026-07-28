import asyncio
import pygame

from .exit_codes import *
from .utils.input import Keys

dt = 0.0
FPS = 60

async def Title_Screen(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return SHUT_DOWN

        dt = clock.tick(FPS)//1000
        update(dt)
        render(screen)

        await asyncio.sleep(0)

def update(dt:float):
    pass

def render(screen:pygame.Surface):
    screen.fill("black")
    #renders

    #update screen
    pygame.display.flip()
