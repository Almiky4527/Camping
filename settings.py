import pygame as pg

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRAY = 60, 60, 60
LIGHT_GRAY = 120, 120, 120
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
SNOW_WHITE = 142, 163, 177
SPRING = 90, 160, 70

# Fonts
DEBUG_FONT = "consolas", 12
INVENTORY_FONT = "consolas", 16

# Display
SCREEN_RES = 1200, 750 # 1920, 1080 - 1280, 720
SCREEN_CENTER = SCREEN_RES[0] // 2, SCREEN_RES[1] // 2
SCREEN_CAPTION = "Camping"
FPS = 60
SCALE = 3
SLOT_POS = 45, 45


# *** Identifiers ***

# Players
PLAYER0 = 0
# Animals
ANIMAL0 = 0
# Items
LOG = 0
STICK = 1
AXE = 2
# Foliage
PINE0 = 0
PINE1 = 1
PINE2 = 2
# Rocks
ROCK0 = 0
# Inventory
SLOT = 0
SLOT_PLUS = 1
SLOT_EQUALS = 2

# *** ----------- ***


def directionalize(v2):
    v = pg.math.Vector2(v2)
    v.x = v.x // abs(v.x) if v.x != 0 else 0
    v.y = v.y // abs(v.y) if v.y != 0 else 0
    return v


def position_from_screen(position, camera_topleft):
    return pg.math.Vector2(position) + camera_topleft


def position_to_screen(position, camera_topleft):
    return pg.math.Vector2(position) - camera_topleft


def print_(surface, text, font, color, bg=None, aa=True, topleft=None, center=None):
    if not topleft and not center:
        raise Exception("position must be provided (topleft or center)")

    render = font.render( str(text), aa, color, bg )
    rect = render.get_rect()

    if topleft:
        rect.topleft = topleft
    elif center:
        rect.center = center

    surface.blit(render, rect)


class Object:

    def __init__(self, image, position, parent):
        self.image = image
        self.box = self.image.get_rect(midbottom = position)
        self.rect = self.box.copy()
        self.parent = parent
        
    @property
    def position(self):
        return self.box.midbottom

    def set_position(self, position):
        self.box.midbottom = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass
