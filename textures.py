import pygame as pg
from settings import *


PATH_PLAYERS = ".\\Textures\\Players.png"
PATH_ANIMALS = ".\\Textures\\Animals.png"
PATH_ITEMS = ".\\Textures\\Items.png"
PATH_FOLIAGE = ".\\Textures\\Foliage.png"
PATH_ROCKS = ".\\Textures\\Rocks.png"
PATH_INVENTORY = ".\\Textures\\Inventory.png"


# Players
PLAYERS = [
    pg.Rect(0, 0, 12, 28)
]

# Animals
ANIMALS = []

# Items
ITEMS = [
    pg.Rect(1, 1, 16, 16),
    pg.Rect(1 + 17 * 1, 1, 16, 16),
    pg.Rect(1 + 17 * 2, 1, 16, 16),
    pg.Rect(1 + 17 * 3, 1, 16, 16)
]

# Foliage
FOLIAGE = [
    pg.Rect(1, 1, 44, 95),
    pg.Rect(54, 1, 28, 70),
    pg.Rect(83, 1, 31, 110)
]

# Rocks
ROCKS = []

# Inventory
INVENTORY = [
    pg.Rect(1, 1, 22, 22),
    pg.Rect(24, 1, 22, 22),
    pg.Rect(47, 1, 22, 22)
]


def scale_(surface, scale):
    w, h = surface.get_size()
    new_size = ( w * scale, h * scale )
    return pg.transform.scale(surface, new_size)


def crop_(surface, rect):
    if type(rect) != pg.Rect:
        raise TypeError("arg 'rect' (2) must be of type pygame.Rect")

    subsurface = surface.subsurface(rect)
    return subsurface


def make_texture(img, scale = None, rect = None, colorkey = BLACK):
    if type(img) == str:
        img = pg.image.load(img)
    elif type(img) != pg.Surface:
        raise TypeError("arg 'img' (1) must be either of type str (path to file) or pygame.Surface")

    img = img.convert()

    if rect:
        img = crop_(img, rect)
    if colorkey:
        img.set_colorkey(colorkey)
    if scale:
        img = scale_(img, scale)
        
    return img


class TextureContainer:

    def __init__(self):
        self.players = []
        self.animals = []
        self.items = []
        self.foliage = []
        self.rocks = []
        self.inventory = []
        self.setup()

    def setup(self, scale=SCALE):
        players = pg.image.load(PATH_PLAYERS)
        animals = pg.image.load(PATH_ANIMALS)
        items = pg.image.load(PATH_ITEMS)
        foliage = pg.image.load(PATH_FOLIAGE)
        rocks = pg.image.load(PATH_ROCKS)
        inventory = pg.image.load(PATH_INVENTORY)

        for rect in PLAYERS:
            texture = make_texture(players, scale, rect)
            self.players.append(texture)

        for rect in ANIMALS:
            texture = make_texture(animals, scale, rect)
            self.animals.append(texture)

        for rect in ITEMS:
            texture = make_texture(items, scale, rect)
            self.items.append(texture)

        for rect in FOLIAGE:
            texture = make_texture(foliage, scale, rect)
            self.foliage.append(texture)

        for rect in ROCKS:
            texture = make_texture(rocks, scale, rect)
            self.rocks.append(texture)

        for rect in INVENTORY:
            texture = make_texture(inventory, scale, rect)
            self.inventory.append(texture)

        self.debug_font = pg.font.SysFont(*DEBUG_FONT)
        self.inventory_font = pg.font.SysFont(*INVENTORY_FONT)
