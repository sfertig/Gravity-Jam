import asyncio
import pygame
from random import choice

from .exit_codes import *
from .utils.input import Keys
from .utils.assets import Assets
from .utils.animation import Text

import random

quotes = [
    # General Gravity & Physics Blunders
    "Gravity works both ways, you know.",
    "You flipped when you should have flopped.",
    "Newton is shaking his head right now.",
    "Down became up, and then everything went wrong.",
    "Upside down and out of time!",
    "Physics lesson #1: The floor isn't always below you.",
    "Centrifugal force won't save you here!",
    "That was a gravity-defying mistake.",
    # Lab & Experiment Theme
    "Lab Hazard #402: Sudden Orientation Reversal.",
    "The scientists are writing this down as a failure.",
    "Your lab safety clearance has been revoked.",
    "Experiment #842: Inconclusive (and painful).",
    "Please return your test subject badge at the desk.",
    "OSHA is going to have a field day with this room.",
    "Note to self: Don't press the giant glowing button.",
    # Heavy Objects & Balloons
    "That crate was WAY heavier than it looked.",
    "Squished like a lab pancake!",
    "A bunch of balloons is NOT a bunch of fun.",
    "Death by extreme buoyancy!",
    "Who knew static electricity could be so lethal?",
    "Smothered by party favors.",
    "Flat as an empty beaker.",
    # Spikes & Hazards
    "Watch out for the pointy bits!",
]

dt = 0.0
FPS = 60

bg_color = "purple"

text: list[Text] = []

async def Death_Screen(screen:pygame.Surface, clock:pygame.time.Clock, level_code:int) -> int:
    global text

    text = [
        Text(Assets.get_font("font"), choice(quotes), (201, 159, 159), 12, 16, 0),
        Text(Assets.get_font("font"), "(press enter to restart)", "white", 12, 16, 16),
        Text(Assets.get_font("font"), "(press escape to quit)", "white", 12, 16, 32),
    ]
    
    while True:
        events = pygame.event.get().copy()
        for event in events:
            if event.type == pygame.QUIT: return SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): return TITLE_SCREEN
        if Keys.is_pressed(Keys.enter, events): return level_code

        dt = clock.tick(FPS)//1000
        update(dt)
        render(screen)

        await asyncio.sleep(0)

def update(dt:float):
    pass

def render(screen:pygame.Surface):
    screen.fill(bg_color)
    #renders
    screen.blit(Assets.get_image("death"), (0, 0))

    for t in text:
        t.render(screen)
    #update screen
    pygame.display.flip()
