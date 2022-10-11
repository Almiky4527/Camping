import pygame as pg
from settings import *


class Camera:

    def __init__(self, parent):
        self.parent = parent
        self.box = self.screen.get_rect().copy()

    @property
    def screen(self):
        return self.parent.screen

    @property
    def world(self):
        return self.parent.world

    @property
    def player(self):
        return self.parent.player

    @property
    def center(self):
        return self.box.center

    @property
    def topleft(self):
        return self.box.topleft

    @property
    def scene(self):
        return sorted(
            filter(self.is_on_camera, self.world.children),
            key = lambda child : child.box.bottom
        )

    def is_on_camera(self, obj):
        return obj.box.colliderect(self.box)

    def get_debug(self):
        if not self.parent.debug_mode:
            return

        draw_reach = self.player.reach.copy()
        draw_reach.center = position_to_screen(draw_reach.center, self.topleft)
        pg.draw.rect(self.screen, RED, draw_reach, 2)

    def draw(self):
        for child in self.scene:
            child.rect.midbottom = position_to_screen(child.position, self.topleft)
            child.draw(self.screen)
            
    def run(self, position):
        self.box.center = position
        
