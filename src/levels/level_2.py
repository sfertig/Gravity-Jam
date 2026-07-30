import asyncio
import pygame

from ..exit_codes import *
from ..utils.input import Keys
from ..utils.assets import Assets
from ..objs.player import Player
from ..utils.math.vector import Vector2D
from ..objs.collisions import Collisions
from ..utils.animation import Text

from ..objs.gravityObj import Box, Balloon

dt = 0.0
FPS = 60

gravity = 130.0

bg_color = "blue"
coll = Collisions(16, "data/level_2_collisions.json", False)

goal = pygame.Rect(352, 304, 32, 32)

player = Player(16, 16, gravity, coll)

boxes: list[Box] = []
balloons: list[Balloon] = []

btn_image: pygame.Surface
btn_image_pos = Vector2D(0, 0)

def reset():
    global dt
    global FPS
    global gravity
    global bg_color
    global coll
    global goal
    global player
    global boxes
    global balloons
    global text
    global btn_image
    global btn_image_pos
    dt = 0.0
    FPS = 60

    gravity = 130.0

    bg_color = "blue"
    coll = Collisions(16, "data/level_2_collisions.json", False)

    goal = pygame.Rect(352, 304, 32, 32)

    player = Player(16, 16, gravity, coll)

    boxes= []
    balloons = []

    text = None

    btn_image = None
    btn_image_pos = Vector2D(0, 0)

def create_objs():
    global boxes
    boxes = [
    ]
    for x in range(16, 336, 16):
        boxes.append(Box(x, 32, gravity, coll, Assets.get_image("box")))

    global balloons
    balloons = [
        Balloon(368, 80, gravity, coll, Assets.get_image("balloon")),
    ]

def load_assets():
    player.load_assets()
    Assets.new_image("bg", "images/level_2.png")
    Assets.new_image("btn_down", "images/button_ui_down.png")
    Assets.new_image("btn_up", "images/button_ui_up.png")
    Assets.new_image("box", "images/box.png")
    Assets.new_image("balloon", "images/balloon.png")
    Assets.new_image("death", "images/death_screen.png")

    Assets.new_font("font", "fonts/font.ttf", 20)

async def Level_2(screen:pygame.Surface, clock:pygame.time.Clock) -> int:
    global btn_image
    reset()
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
            if event.type == pygame.QUIT: return SHUT_DOWN, TITLE_SCREEN

        if Keys.is_pressed(Keys.escape, events): return TITLE_SCREEN, TITLE_SCREEN

        dt = clock.tick(FPS)/1000.0
        num = update(dt, events)
        render(screen)

        if num != None: return num, LEVEL_2

        await asyncio.sleep(0)

def change_gravity():
    global gravity
    global btn_image

    gravity *= -1
    player.change_gravity(gravity)
    for box in boxes:
        box.change_gravity(gravity)
    for balloon in balloons:
        balloon.change_gravity(gravity)
    if gravity > 0: btn_image = Assets.get_image("btn_down")
    else: btn_image = Assets.get_image("btn_up")

def get_rects():
    global boxes
    rects = []
    for box in boxes:
        rects.append(box.rect())
    return rects

def balloon_rects():
    global balloons
    rects = []
    for balloon in balloons:
        rects.append(balloon.rect())
    return rects

def update(dt:float, events):
    num = player.update(dt, events, get_rects(), balloon_rects())
    coll.update(events)

    for box in boxes:
        box.update(dt, events)

    for balloon in balloons:
        balloon.update(dt, events)

    if player.rect().colliderect(goal): return LEVEL_3

    if Keys.is_pressed(Keys.space, events) and player.on_floor: change_gravity()
    return num

def render(screen:pygame.Surface):
    global text
    screen.fill(bg_color)
    screen.blit(Assets.get_image("bg"), (0, 0))
    #renders
    player.render(screen)

    for box in boxes:
        box.render(screen)

    for balloon in balloons:
        balloon.render(screen)

    coll.render(screen)

    pygame.draw.rect(screen, "green", goal, 1)

    screen.blit(btn_image, btn_image_pos.to_int())
    #update screen
    pygame.display.flip()
