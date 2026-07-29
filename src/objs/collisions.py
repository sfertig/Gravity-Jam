import pygame
import json

from ..utils.input import Keys
from ..utils.math.vector import Vector2D

DETAIL = 3

class _tiles:
    def __init__(self, size):
        self.size = size
        self.gen_tiles()

    def get_tile(self, num):
        if num == 1: return self.full
        elif num == 2: return self.half_top
        elif num == 3: return self.half_bottom
        elif num == 4: return self.half_left
        elif num == 5: return self.half_right

    def get_num(self, rect):
        if rect.size == self.full.size: return 1
        elif rect.size == self.half_top.size: return 2
        elif rect.size == self.half_bottom.size: return 3
        elif rect.size == self.half_left.size: return 4
        elif rect.size == self.half_right.size: return 5

    def gen_tiles(self):
        s = self.size
        self.full = pygame.Rect(0, 0, s, s)
        self.half_top = pygame.Rect(0, 0, s, s//2)
        self.half_bottom = pygame.Rect(0, s//2, s, s//2)
        self.half_left = pygame.Rect(0, 0, s//2, s)
        self.half_right = pygame.Rect(s//2, 0, s//2, s)

def load_json(path, tiles: _tiles):
    with open(path, "r") as f:
        save = json.load(f)
    #data is dict[list[int, int], int]
    data = {}
    for pos, value in save.items():
        p = tuple(map(int, pos.split(";")))
        rect = tiles.get_tile(value).copy()
        rect.x = p[0]
        rect.y = p[1]
        data[p] = rect

    return data

def save_json(path, data, tiles):
    save = {}
    for pos, rect in data.items():
        p = str(pos[0])+";"+str(pos[1])
        save[p] = tiles.get_num(rect)
    with open(path, "w") as f:
        json.dump(save, f)

class Collisions:
    def __init__(self, size, file=None, build=False):
        self.size = size
        self.path = file
        self._tiles = _tiles(self.size)
        self.tiles: dict[list[int, int], pygame.Rect] = {}
        if file is not None:
            self.tiles = load_json(file, self._tiles)

        self.active = False
        self.build = build

        if not build: self.cur_tile = self._tiles.full.copy()
        else: self.cur_tile = None

    def update(self, events):
        if self.build: return
        if Keys.is_pressed(Keys.n0, events): 
            self.active = not self.active
            save_json(self.path, self.tiles, self._tiles)

        if not self.active: return

        if pygame.mouse.get_pressed()[0]:
            self.tiles[self.cur_tile.x, self.cur_tile.y] = self.cur_tile.copy()
        elif pygame.mouse.get_pressed()[2]:
            if (self.cur_tile.x, self.cur_tile.y) in self.tiles: del self.tiles[self.cur_tile.x, self.cur_tile.y]

        #change tile based on number pressed
        if Keys.is_pressed(Keys.n1, events): self.cur_tile = self._tiles.full.copy()
        elif Keys.is_pressed(Keys.n2, events): self.cur_tile = self._tiles.half_top.copy()
        elif Keys.is_pressed(Keys.n3, events): self.cur_tile = self._tiles.half_bottom.copy()
        elif Keys.is_pressed(Keys.n4, events): self.cur_tile = self._tiles.half_left.copy()
        elif Keys.is_pressed(Keys.n5, events): self.cur_tile = self._tiles.half_right.copy()
        

    def get_tiles_around(self, pos:Vector2D):
        x = (pos.x//self.size)*self.size
        y = (pos.y//self.size)*self.size
        around = []
        for i in range(-DETAIL, DETAIL):
            _y=y+(i*self.size)
            for j in range(-DETAIL, DETAIL):
                _x=x+(j*self.size)
                if (_x, _y) in self.tiles: around.append(self.tiles[_x, _y])

        return around
        


    def render(self, screen:pygame.Surface):
        if self.build or not self.active: return

        pygame.draw.rect(screen, "red", screen.get_rect().copy(), 1)

        for pos, rect in self.tiles.items():
            r = rect.copy()
            pygame.draw.rect(screen, "yellow", r, 1)

        #render current tile
        self.cur_tile.x = ((pygame.mouse.get_pos()[0])//self.size)*self.size
        self.cur_tile.y = ((pygame.mouse.get_pos()[1])//self.size)*self.size
        pygame.draw.rect(screen, "green", self.cur_tile, 1)
