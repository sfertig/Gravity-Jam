import asyncio
import pygame
import sys

from src.exit_codes import *
from src.title_screen import Title_Screen
from src.levels.level_1 import Level_1

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
    
    state = TITLE_SCREEN
    while True:
        if state == TITLE_SCREEN: state = await Title_Screen(screen, clock)
        elif state == SHUT_DOWN: break
        elif state == LEVEL_1: state = await Level_1(screen, clock)
    pygame.quit()

asyncio.run(main())
