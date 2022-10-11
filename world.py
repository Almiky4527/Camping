import pygame as pg
from random import randrange, random, choice
from settings import *
from textures import *
from terrain import *
from player import *
from items import *


class World:

    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.background_color = SPRING
        self.generate()

    @property
    def player(self):
        return self.parent.player

    @property
    def camera(self):
        return self.parent.camera

    @property
    def texture_container(self):
        return self.parent.texture_container

    def add_child(self, obj):
        self.children.append(obj)

    def remove_child(self, obj):
        self.children.remove(obj)

    def generate(self):
        r = 10000
        scatter = -r, r

        for x in range(10000):
            iid = randrange(1, 3)
            texture = self.texture_container.foliage[iid]
            spawn_pos = ( randrange(*scatter), randrange(*scatter) )
            pine = Tree(iid, texture, spawn_pos, self)
            self.add_child(pine)

    def spawn_item(self, iid, position, count=1, sx=None, sy=None):
        texture = self.texture_container.items[iid]
        
        spawn_pos = list(position).copy()
        spawn_pos[0] += randrange(-sx, sx) if sx else 0
        spawn_pos[1] += randrange(-sy, sy) if sy else 0
        
        item = Item(iid, count, texture, spawn_pos, self)
        self.add_child(item)

    def draw(self, screen):
        screen.fill(self.background_color)

    def run(self):
        for child in self.children:
            child.update()
        
