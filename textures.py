from pygame import Rect, image
from pygame.font import SysFont
import pygame.freetype

from os import path
from inventory import *
from entities import *

from utils.functions import *
from utils.display import SCALE
from utils.classes import TextureTypeError


# --- Fonts ---
DEBUG_FONT = "consolas", 12
INVENTORY_FONT = "consolas", 16
STORY_FONT = "consolas", 20
STORY_FONT_CUTSCENES = "consolas", 28
TITLE_FONT = "consolas", 30
# -------------


SHADOWS_OPACITY = 50

FOLIAGE_ROW_Y = 1

PLAYER_ROW_1_Y = 257
PLAYER_ROW_2_Y = 286

ITEM_ROW_1_Y = 214
ITEM_ROW_2_Y = 231

ANIMAL_ROW_Y = 464
ANIMAL_ROW_2_Y = 480
ANIMAL_ROW_3_Y = 506

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
        ],
    },
    "JaneSmith": {
        SOUTH: [
            Rect(1, PLAYER_ROW_2_Y, 12, 28),
            Rect(14, PLAYER_ROW_2_Y, 12, 28),
            Rect(27, PLAYER_ROW_2_Y, 12, 28),
        ],
        NORTH: [
            Rect(40, PLAYER_ROW_2_Y, 12, 28),
            Rect(53, PLAYER_ROW_2_Y, 12, 28),
            Rect(66, PLAYER_ROW_2_Y, 12, 28),
        ],
        EAST: [
            Rect(79, PLAYER_ROW_2_Y, 12, 28),
            Rect(92, PLAYER_ROW_2_Y, 12, 28),
            Rect(105, PLAYER_ROW_2_Y, 12, 28),
        ],
        WEST: [
            Rect(118, PLAYER_ROW_2_Y, 12, 28),
            Rect(131, PLAYER_ROW_2_Y, 12, 28),
            Rect(144, PLAYER_ROW_2_Y, 12, 28),
        ],
    },
    "item": {
        DEFAULT: Rect(1, ITEM_ROW_1_Y, 16, 16),
        ITEM_LOG: Rect(18, ITEM_ROW_1_Y, 16, 16),
        ITEM_STICK: Rect(35, ITEM_ROW_1_Y, 16, 16),
        ITEM_AXE: Rect(52, ITEM_ROW_1_Y, 16, 16),
        ITEM_IMPROVISED_AXE: Rect(307, ITEM_ROW_1_Y, 16, 16),
        ITEM_TENT: Rect(69, ITEM_ROW_1_Y, 16, 16),
        ITEM_CABIN_PLAN: Rect(324, ITEM_ROW_1_Y, 16, 16),
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
        STONE: Rect(120, ITEM_ROW_1_Y, 16, 16),
        ITEM_THREAD: Rect(137, ITEM_ROW_1_Y, 16, 16),
        ITEM_ROPE: Rect(154, ITEM_ROW_1_Y, 16, 16),
        ITEM_JACKET: Rect(171, ITEM_ROW_1_Y, 16, 16),
        ITEM_HAT: Rect(188, ITEM_ROW_1_Y, 16, 16),
        ITEM_BERRIES0: Rect(154, ITEM_ROW_2_Y, 16, 16),
        ITEM_BLUEBERRIES: Rect(171, ITEM_ROW_2_Y, 16, 16),
        ITEM_HARE_MEAT: Rect(188, ITEM_ROW_2_Y, 16, 16),
        ITEM_HARE_MEAT_COOKED: Rect(205, ITEM_ROW_2_Y, 16, 16),
        ITEM_DEER_MEAT: Rect(222, ITEM_ROW_2_Y, 16, 16),
        ITEM_DEER_MEAT_COOKED: Rect(239, ITEM_ROW_2_Y, 16, 16),
        ITEM_HARE_HIDE: Rect(273, ITEM_ROW_2_Y, 16, 16),
        ITEM_DEER_HIDE: Rect(290, ITEM_ROW_2_Y, 16, 16),
        ITEM_ROCK_TRAP: Rect(205, ITEM_ROW_1_Y, 16, 16),
        ITEM_ROCK_TRAP_PRIMED: Rect(222, ITEM_ROW_1_Y, 16, 16),
        ITEM_NOOSE_TRAP: Rect(239, ITEM_ROW_1_Y, 16, 16),
        ITEM_FEATHER: Rect(256, ITEM_ROW_2_Y, 16, 16),
        ITEM_STONE_BLADE: Rect(290, ITEM_ROW_1_Y, 16, 16),
        ITEM_BOW: Rect(256, ITEM_ROW_1_Y, 16, 16),
        ITEM_ARROW: Rect(273, ITEM_ROW_1_Y, 16, 16),
        ITEM_4D617877656C6C: Rect(358, ITEM_ROW_2_Y, 16, 16),
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

        "autumn." + PINE_SMALL: Rect(217, FOLIAGE_ROW_Y, 28, 70),
        "autumn." + PINE_LARGE: Rect(185, FOLIAGE_ROW_Y, 31, 110),
        "autumn." + OAK_SMALL: Rect(347, FOLIAGE_ROW_Y, 35, 67),
        "autumn." + OAK_LARGE: Rect(309, FOLIAGE_ROW_Y, 37, 100),

        "winter." + PINE_SMALL: Rect(278, FOLIAGE_ROW_Y, 28, 70),
        "winter." + PINE_LARGE: Rect(246, FOLIAGE_ROW_Y, 31, 110),
        "winter." + OAK_SMALL: Rect(347, FOLIAGE_ROW_Y, 35, 67),
        "winter." + OAK_LARGE: Rect(309, FOLIAGE_ROW_Y, 37, 100),
        "winter." + BUSH_LARGE: Rect(136, 69, 30, 18),
        "winter." + BUSH_SMALL: Rect(136, 88, 20, 14),
    },
    "inventory": {
        SLOT_DEFAULT: Rect(1, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_PLUS: Rect(24, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_EQUALS: Rect(47, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_WEAR_JACKET: Rect(70, INVENTORY_ROW_1_Y, 22, 22),
        SLOT_WEAR_HAT: Rect(93, INVENTORY_ROW_1_Y, 22, 22),
    },
    "objects": {
        DEFAULT: Rect(1, OBJECTS_ROW_1_Y, 26, 26),
        ENTITY_TENT: Rect(28, OBJECTS_ROW_1_Y, 54, 39),
        ENTITY_CAMPFIRE: Rect(83, OBJECTS_ROW_1_Y, 18, 19),
        ENTITY_CABIN_FOUNDATION: Rect(209, OBJECTS_ROW_1_Y, 62, 22),
        ENTITY_CABIN: Rect(140, OBJECTS_ROW_1_Y, 68, 70),
        "winter." + ENTITY_CABIN: Rect(272, OBJECTS_ROW_1_Y, 68, 70),
        ENTITY_ROCK_TRAP: Rect(49, 174, 15, 12),
        ENTITY_NOOSE_TRAP: Rect(28, 170, 20, 16),
        ENTITY_ARROW: Rect(67, 170, 15, 16),
    },
    "shadows": {
        SHADOW_SMALL: Rect(1, SHADOWS_ROW_Y, 12, 3),
        SHADOW_MEDIUM: Rect(14, SHADOWS_ROW_Y, 18, 6),
        SHADOW_ITEM: Rect(14, SHADOWS_ROW_Y + 7, 18, 4),
        SHADOW_PLANT: Rect(8, SHADOWS_ROW_Y + 4, 5, 3),

        SHADOW_SUBTYPE + STONE: Rect(1, 342, 12, 4),

        SHADOW_SUBTYPE + ENTITY_TENT: Rect(33, SHADOWS_ROW_Y, 56, 24),
        SHADOW_SUBTYPE + ENTITY_CAMPFIRE: Rect(14, SHADOWS_ROW_Y + 12, 18, 8),
        SHADOW_SUBTYPE + ENTITY_CABIN_FOUNDATION: Rect(188, SHADOWS_ROW_Y, 64, 40),
        SHADOW_SUBTYPE + ENTITY_CABIN: Rect(121, SHADOWS_ROW_Y, 66, 38),

        SHADOW_SUBTYPE + BUSH_LARGE: Rect(90, SHADOWS_ROW_Y, 30, 6),
        SHADOW_SUBTYPE + BUSH_SMALL: Rect(90, SHADOWS_ROW_Y + 7, 20, 6),

        SHADOW_SUBTYPE + ANIMAL_HARE: Rect(0, 332, 13, 9),
        SHADOW_SUBTYPE + ANIMAL_DEER: [
            Rect(63, 351, 9, 14),
            Rect(73, 351, 9, 14),
            Rect(40, 355, 22, 3),
            Rect(40, 351, 22, 3),
        ],
        SHADOW_SUBTYPE + ANIMAL_BEAR: [
            Rect(266, 324, 16, 20),
            Rect(283, 324, 16, 20),
            Rect(300, 324, 30, 6),
            Rect(300, 331, 30, 6),
        ],

        SHADOW_SUBTYPE + ENTITY_ROCK_TRAP: Rect(331, SHADOWS_ROW_Y, 17, 5),
        SHADOW_SUBTYPE + ENTITY_NOOSE_TRAP: Rect(349, SHADOWS_ROW_Y, 23, 3),
        SHADOW_SUBTYPE + ENTITY_ARROW: Rect(253, SHADOWS_ROW_Y, 12, 4),
    },
    ENTITY_CAMPFIRE + BURNING_SUBTYPE: {
        SOUTH: [
            Rect(102, OBJECTS_ROW_1_Y, 18, 19),
            Rect(121, OBJECTS_ROW_1_Y, 18, 19),
        ],
    },
    "animal": {
        SOUTH: [
            Rect(1, ANIMAL_ROW_Y, 12, 12),
            Rect(14, ANIMAL_ROW_Y, 12, 12),
            Rect(27, ANIMAL_ROW_Y, 12, 12),
        ],
        NORTH: [
            Rect(40, ANIMAL_ROW_Y, 12, 12),
            Rect(53, ANIMAL_ROW_Y, 12, 12),
            Rect(66, ANIMAL_ROW_Y, 12, 12),
        ],
        EAST: [
            Rect(79, ANIMAL_ROW_Y, 12, 12),
            Rect(92, ANIMAL_ROW_Y, 12, 12),
            Rect(105, ANIMAL_ROW_Y, 12, 12),
        ],
        WEST: [
            Rect(118, ANIMAL_ROW_Y, 12, 12),
            Rect(131, ANIMAL_ROW_Y, 12, 12),
            Rect(144, ANIMAL_ROW_Y, 12, 12),
        ],
    },
    ANIMAL_HARE: {
        SOUTH: [
            Rect(187, ANIMAL_ROW_Y, 9, 9),
            Rect(197, ANIMAL_ROW_Y, 9, 9),
        ],
        NORTH: [
            Rect(237, ANIMAL_ROW_Y, 9, 9),
            Rect(247, ANIMAL_ROW_Y, 9, 9),
        ],
        EAST: [
            Rect(207, ANIMAL_ROW_Y, 14, 9),
            Rect(222, ANIMAL_ROW_Y, 14, 9),
        ],
        WEST: [
            Rect(157, ANIMAL_ROW_Y, 14, 9),
            Rect(172, ANIMAL_ROW_Y, 14, 9),
        ],
    },
    ANIMAL_DEER: {
        SOUTH: [
            Rect(1, ANIMAL_ROW_2_Y, 7, 22),
            Rect(9, ANIMAL_ROW_2_Y, 7, 22),
            Rect(17, ANIMAL_ROW_2_Y, 7, 22),
        ],
        NORTH: [
            Rect(25, ANIMAL_ROW_2_Y, 7, 22),
            Rect(33, ANIMAL_ROW_2_Y, 7, 22),
            Rect(41, ANIMAL_ROW_2_Y, 7, 22),
        ],
        EAST: [
            Rect(49, ANIMAL_ROW_2_Y, 25, 21),
            Rect(75, ANIMAL_ROW_2_Y, 25, 21),
            Rect(101, ANIMAL_ROW_2_Y, 25, 21),
        ],
        WEST: [
            Rect(127, ANIMAL_ROW_2_Y, 25, 21),
            Rect(153, ANIMAL_ROW_2_Y, 25, 21),
            Rect(179, ANIMAL_ROW_2_Y, 25, 21),
        ],
    },
    ANIMAL_BEAR: {
        SOUTH: [
            Rect(1, ANIMAL_ROW_3_Y, 14, 22),
            Rect(16, ANIMAL_ROW_3_Y, 14, 22),
            Rect(31, ANIMAL_ROW_3_Y, 14, 22),
        ],
        NORTH: [
            Rect(46, ANIMAL_ROW_3_Y, 14, 22),
            Rect(61, ANIMAL_ROW_3_Y, 14, 22),
            Rect(76, ANIMAL_ROW_3_Y, 14, 22),
        ],
        EAST: [
            Rect(91, ANIMAL_ROW_3_Y, 30, 18),
            Rect(122, ANIMAL_ROW_3_Y, 30, 18),
            Rect(153, ANIMAL_ROW_3_Y, 30, 18),
        ],
        WEST: [
            Rect(184, ANIMAL_ROW_3_Y, 30, 18),
            Rect(215, ANIMAL_ROW_3_Y, 30, 18),
            Rect(246, ANIMAL_ROW_3_Y, 30, 18),
        ],
    },
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
            if type(texture) == list:
                for _texture in texture:
                    _texture.set_alpha(SHADOWS_OPACITY)
            else:
                texture.set_alpha(SHADOWS_OPACITY)
            
        def _insert_frame(texture_set : dict, grab_index : int, insert_index : int):
            for texture_list in texture_set.values():
                frame = texture_list[grab_index]
                texture_list.insert(insert_index, frame)

        _insert_frame( self["JohnDoe"], 0, 2 )
        _insert_frame( self["JaneSmith"], 0, 2 )
        _insert_frame( self["animal"], 0, 2 )
        _insert_frame( self[ANIMAL_DEER], 0, 2 )
        _insert_frame( self[ANIMAL_BEAR], 0, 2 )

        self.debug_font = SysFont(*DEBUG_FONT)
        self.inventory_font = SysFont(*INVENTORY_FONT)
        self.story_font = SysFont(*STORY_FONT)
        self.story_font_cutscenes = SysFont(*STORY_FONT_CUTSCENES)
        self.title_font = SysFont(*TITLE_FONT)

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
    
    def get_animal_set(self, key):
        return self[key] if key in self.sets else self["animal"]

    def texture(self, set_name, key=None):
        '''Return the texture for key if key is in sets, else default.'''
        textureset = self[set_name]
        default_texture = textureset[0]
        return textureset.get(key, default_texture)
