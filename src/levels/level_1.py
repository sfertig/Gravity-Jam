import asyncio
import pygame

from ..exit_codes import *
from ..utils.input import Keys
from ..utils.assets import Assets
from ..objs.player import Player
from ..utils.math.vector import Vector2D
from ..objs.collisions import Collisions

from ..objs.gravityObj import Box

dt = 0.0
FPS = 60

gravity = 130.0

bg_color = "blue"
coll = Collisions(16, "data/level_1_collisions.json", False)

player = Player(0, 100, gravity, coll)

boxes: list[Box] = []

btn_image: pygame.Surface
btn_image_pos = Vector2D(0, 0)

def create_objs():
    global boxes
    boxes = [
        Box(100, 300, gravity, coll, Assets.get_image("box")),
]

def load_assets():
    player.load_assets()
    Assets.new_image("bg", "images/level_1_bg.png")
    Assets.new_image("btn_down", "images/button_ui_down.png")
    Assets.new_image("btn_up", "images/button_ui_up.png")
    Assets.new_image("box", "images/box.png")




async def Level_1(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    global btn_image
    load_assets()
    create_objs()
    #set btn pos
    btn_image = Assets.get_image("btn_down")
    dim = btn_image.get_size()
    btn_image_pos.x = screen.get_width() - dim[0]
    btn_image_pos.y = screen.get_height() - dim[1]
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return SHUT_DOWN   #TITLE_SCREEN

        dt = clock.tick(FPS)/1000.0
        update(dt, events)
        render(screen)

        await asyncio.sleep(0)

def change_gravity():
    global gravity
    global btn_image
    gravity *= -1
    player.change_gravity(gravity)
    for box in boxes:
        box.change_gravity(gravity)
    if gravity > 0: btn_image = Assets.get_image("btn_down")
    else: btn_image = Assets.get_image("btn_up")


def get_rects():
    global boxes
    rects = []
    for box in boxes:
        rects.append(box.rect())
    return rects

def update(dt:float, events):

    if Keys.is_pressed(Keys.e, events): change_gravity()
    player.update(dt, events, get_rects())
    coll.update(events)

    for box in boxes:
        box.update(dt, events)

def render(screen:pygame.Surface):
    screen.fill(bg_color)
    screen.blit(Assets.get_image("bg"), (0, 0))
    #renders
    player.render(screen)

    for box in boxes:
        box.render(screen)

    coll.render(screen)

    screen.blit(btn_image, btn_image_pos.to_int())
    #update screen
    pygame.display.flip()
