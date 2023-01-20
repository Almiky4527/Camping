from pygame import Rect, image
from pygame.font import SysFont

from os import path
from inventory import *
from entities import *

from utils.functions import *
from utils.classes import TextureTypeError


# --- Fonts ---
DEBUG_FONT = "consolas", 12
INVENTORY_FONT = "consolas", 16
STORY_FONT = "consolas", 20
# -------------


SHADOWS_OPACITY = 50

FOLIAGE_ROW_Y = 1

PLAYER_ROW_1_Y = 257
PLAYER_ROW_2_Y = 286

ITEM_ROW_1_Y = 214
ITEM_ROW_2_Y = 231

INVENTORY_ROW_1_Y = 384

OBJECTS_ROW_1_Y = 128

SHADOWS_ROW_Y = 324


TEXTURES_RECTS = {
    "JohnDoe": {
        SOUTH: [
            Rect(1, PLAYER_ROW_1_Y, 12, 28),
            Rect(14, PLAYER_ROW_1_Y, 12, 28),
            Rect(27, PLAYER_ROW_1_Y, 12, 28),
        ],
        NORTH: [
            Rect(40, PLAYER_ROW_1_Y, 12, 28),
            Rect(53, PLAYER_ROW_1_Y, 12, 28),
            Rect(66, PLAYER_ROW_1_Y, 12, 28),
        ],
        EAST: [
            Rect(79, PLAYER_ROW_1_Y, 12, 28),
            Rect(92, PLAYER_ROW_1_Y, 12, 28),
            Rect(105, PLAYER_ROW_1_Y, 12, 28),
        ],
        WEST: [
            Rect(118, PLAYER_ROW_1_Y, 12, 28),
            Rect(131, PLAYER_ROW_1_Y, 12, 28),
            Rect(144, PLAYER_ROW_1_Y, 12, 28),
        ]
    },
    "animals": {},
    "item": {
        DEFAULT: Rect(1, ITEM_ROW_1_Y, 16, 16),
        ITEM_LOG: Rect(18, ITEM_ROW_1_Y, 16, 16),
        ITEM_STICK: Rect(35, ITEM_ROW_1_Y, 16, 16),
        ITEM_AXE: Rect(52, ITEM_ROW_1_Y, 16, 16),
        ITEM_TENT: Rect(69, ITEM_ROW_1_Y, 16, 16),
        ITEM_CAMPFIRE: Rect(86, ITEM_ROW_1_Y, 16, 16),
        ITEM_MATCHES: Rect(103, ITEM_ROW_1_Y, 16, 16),
        ROCK0: Rect(1, ITEM_ROW_2_Y, 16, 16),
        ROCK1: Rect(18, ITEM_ROW_2_Y, 16, 16),
        ROCK2: Rect(35, ITEM_ROW_2_Y, 16, 16),
        ROCK3: Rect(52, ITEM_ROW_2_Y, 16, 16),
        ROCK4: Rect(69, ITEM_ROW_2_Y, 16, 16),
        ITEM_PLANT0: Rect(86, ITEM_ROW_2_Y, 16, 16),
        ITEM_PLANT1: Rect(103, ITEM_ROW_2_Y, 16, 16),
        ITEM_PLANT2: Rect(120, ITEM_ROW_2_Y, 16, 16),
        ITEM_PLANT3: Rect(137, ITEM_ROW_2_Y, 16, 16),
    },
    "foliage": {
        DEFAULT: Rect(1, FOLIAGE_ROW_Y, 28, 70),
        PINE_SMALL: Rect(1, FOLIAGE_ROW_Y, 28, 70),
        PINE_LARGE: Rect(30, FOLIAGE_ROW_Y, 31, 110),
        OAK_SMALL: Rect(62, FOLIAGE_ROW_Y, 35, 67),
        OAK_LARGE: Rect(98, FOLIAGE_ROW_Y, 37, 100),
        BUSH_LARGE: Rect(136, FOLIAGE_ROW_Y, 30, 18),
        BUSH_LARGE + LOOT_SUBTYPE: Rect(136, FOLIAGE_ROW_Y + 19, 30, 18),
        BUSH_SMALL: Rect(136, FOLIAGE_ROW_Y + 38, 20, 14),
        BUSH_SMALL + LOOT_SUBTYPE: Rect(136, FOLIAGE_ROW_Y + 53, 20, 14),
        PLANT0: Rect(167, FOLIAGE_ROW_Y, 7, 21),
        PLANT1: Rect(167, FOLIAGE_ROW_Y + 22, 7, 21),
        PLANT2: Rect(175, FOLIAGE_ROW_Y, 7, 21),
        PLANT3: Rect(175, FOLIAGE_ROW_Y + 22, 7, 21),
    },
    "inventory": {
        SLOT_DEFAULT: Rect(1, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_PLUS: Rect(24, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_EQUALS: Rect(47, INVENTORY_ROW_1_Y, 22, 22)
    },
    "objects": {
        DEFAULT: Rect(1, OBJECTS_ROW_1_Y, 26, 26),
        ENTITY_TENT: Rect(28, OBJECTS_ROW_1_Y, 54, 39),
        ENTITY_CAMPFIRE: Rect(83, OBJECTS_ROW_1_Y, 18, 19),
        ENTITY_CAMPFIRE + BURNING_SUBTYPE: [
            Rect(102, OBJECTS_ROW_1_Y, 18, 19),
            Rect(121, OBJECTS_ROW_1_Y, 18, 19)
        ]
    },
    "shadows": {
        SHADOW_SMALL: Rect(1, SHADOWS_ROW_Y, 12, 3),
        SHADOW_MEDIUM: Rect(14, SHADOWS_ROW_Y, 18, 6),
        SHADOW_ITEM: Rect(14, SHADOWS_ROW_Y + 7, 18, 4),
        SHADOW_PLANT: Rect(8, SHADOWS_ROW_Y + 4, 5, 3),

        SHADOW_SUBTYPE + ENTITY_TENT: Rect(33, SHADOWS_ROW_Y, 56, 24),
        SHADOW_SUBTYPE + ENTITY_CAMPFIRE: Rect(14, SHADOWS_ROW_Y + 12, 18, 8),

        SHADOW_SUBTYPE + BUSH_LARGE: Rect(90, SHADOWS_ROW_Y, 30, 6),
        SHADOW_SUBTYPE + BUSH_SMALL: Rect(90, SHADOWS_ROW_Y + 7, 20, 6),
    }
}


class TextureContainer:
    TEXTURES_FOLDER = "Textures"
    TEXTURES_FILE = "Textures.png"
    PATH = path.join(path.curdir, TEXTURES_FOLDER, TEXTURES_FILE)

    def __init__(self):
        self.sets = {}
        self.setup(SCALE)

    def __getitem__(self, key) -> dict:
        return self.sets[key]
    
    def __contains__(self, value) -> bool:
        return value in self.all
    
    @property
    def all(self):
        all_textures = {}

        for texture_set in self.sets.values():
            all_textures.update(texture_set)

        return all_textures

    def setup(self, scale):
        textures_image = image.load(self.PATH)

        for texture_set_key, texture_set_values in TEXTURES_RECTS.items():
            self.sets[texture_set_key] = {}

            for texture_key, texture_rect_s in texture_set_values.items():
                texture = self.load_texture_from_set(
                    textures_image,
                    texture_rect_s,
                    scale
                )

                if texture:
                    self.sets[texture_set_key][texture_key] = texture
        
        for texture in self["shadows"].values():
            texture.set_alpha(SHADOWS_OPACITY)
        
        for texture_list in self["JohnDoe"].values():
            frame0 = texture_list[0]
            texture_list.insert(2, frame0)

        self.debug_font = SysFont(*DEBUG_FONT)
        self.inventory_font = SysFont(*INVENTORY_FONT)
        self.story_font = SysFont(*STORY_FONT)

    def load_texture_from_set(self, textures_image, rect_s, scale):
        try:
            if type(rect_s) == list:
                return [ make_texture(textures_image, scale, rect) for rect in rect_s ]
            elif type(rect_s) == Rect:
                return make_texture(textures_image, scale, rect_s)
            else:
                return 
        except TypeError:
            raise TextureTypeError(f"incorrect value type for rect(s): { type(rect_s) }, contents of value: {rect_s}")

    def get(self, key):
        if key in self.all:
            return self.all[key]
        else:
            subtype = entity_subtype(key)
            return self.texture(subtype)

    def texture(self, set_name, key=None):
        '''Return the texture for key if key is in sets, else default.'''
        textureset = self[set_name]
        default_texture = textureset[0]
        return textureset.get(key, default_texture)
