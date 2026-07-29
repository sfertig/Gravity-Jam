import asyncio
import pygame
import sys
import os

from src.exit_codes import *
from src.utils.assets import Assets
from src.title_screen import Title_Screen
from src.death_screen import Death_Screen
from src.levels.level_1 import Level_1
from src.levels.level_2 import Level_2

pygame.init()

# Check if running in WebAssembly (Browser)
IS_WEB = sys.platform == "emscripten"

async def main():

    width, height = 640, 360
    if IS_WEB:
        # Web build: rely on SCALED (pygbag handles window fit)
        screen = pygame.display.set_mode((width, height))
    else:
        # Desktop build: full experience with SCALED + FULLSCREEN
        screen = pygame.display.set_mode(
            (width, height), pygame.SCALED | pygame.FULLSCREEN
        )
    pygame.display.set_caption("test title")

    clock = pygame.time.Clock()
    
    state = LEVEL_2
    level = LEVEL_1
    while True:
        if state == TITLE_SCREEN: state = await Title_Screen(screen, clock)
        elif state == SHUT_DOWN: break
        elif state == DEATH_SCREEN: state = await Death_Screen(screen, clock, level)
        elif state == LEVEL_1: 
            state, level = await Level_1(screen, clock)
            Assets._clear(_confirm=True)
        elif state == LEVEL_2: 
            state, level = await Level_2(screen, clock)
            Assets._clear(_confirm=True)
    pygame.quit()

asyncio.run(main())
