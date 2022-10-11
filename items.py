import pygame as pg
from settings import *


MAX_COUNTS = {
    LOG: 8,
    STICK: 32,
    AXE: 1
}


class Item (Object):

    def __init__(self, iid, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iid = iid
        self.count = count

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.count > 1:
            font = self.parent.texture_container.inventory_font
            print_(screen, self.count, font, WHITE, BLACK, center = self.rect.center)
