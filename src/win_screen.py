import asyncio
import pygame

from .exit_codes import *
from .utils.input import Keys
from .utils.animation import Text
from .utils.assets import Assets

dt = 0.0
FPS = 60

bg_color = "green"

async def Win_Screen(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    bg = pygame.image.load("images/win.png")
    text = Text(Assets.get_font("font"), "You Win", "white", 12, 16, 16)
    info = Text(Assets.get_font("font"), "(press enter to return to title screen)", "white", 12, 16, 32)
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return SHUT_DOWN
        if Keys.is_pressed(Keys.enter, events): return LEVEL_1

        dt = clock.tick(FPS)//1000
        update(dt)
        render(screen, bg, text, info)

        await asyncio.sleep(0)

def update(dt:float):
    events = pygame.event.get().copy()
    for event in events:
        if event.type == pygame.QUIT: return SHUT_DOWN
    if Keys.is_pressed(Keys.enter, events): 
        print("enter")
        return TITLE_SCREEN

def render(screen:pygame.Surface, img, text, info):
    print("render")
    screen.fill(bg_color)
    #renders
    screen.blit(img, (0, 0))

    text.render(screen)
    info.render(screen)

    #update screen
    pygame.display.flip()
