import asyncio
import pygame

pygame.init()

width, height = 640, 360
screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("test title")

clock = pygame.time.Clock()



async def main():
    while True:
        pass
    pygame.quit()

asyncio.run(main())
