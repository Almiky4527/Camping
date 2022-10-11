import pygame as pg
from random import randrange, choice
from settings import *
from textures import *
from items import *


class Tree (Object):

    def __init__(self, iid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iid = iid
        self.health = 1000 if iid == PINE1 else 1500 if iid == PINE2 else 100
        self.loot = {
            LOG: range(2, 4),
            STICK: range(0, 3)
        }

    def cut_down(self):
        self.parent.remove_child(self)
        
        for iid in self.loot:
            count = choice(self.loot[iid])
            
            for _ in range(count):
                self.parent.spawn_item(iid, self.position, sx = 40, sy = 30)

    def update(self):
        if self.health <= 0:
            self.cut_down()
