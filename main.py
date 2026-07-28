import asyncio
import pygame

from src.exit_codes import *
from src.title_screen import Title_Screen

pygame.init()

async def main():

    width, height = 640, 360
    screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("test title")

    clock = pygame.time.Clock()
    
    state = TITLE_SCREEN
    while True:
        if state == TITLE_SCREEN:
            state = await Title_Screen(screen, clock)
        elif state == SHUT_DOWN: break
    pygame.quit()

asyncio.run(main())
