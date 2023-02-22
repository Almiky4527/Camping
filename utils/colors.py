try:
    from .identifiers import *
except ImportError:
    from identifiers import *


RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

BLACK = 0, 0, 0
SLIGHTLY_LESS_BLACK = 30, 30, 30
GRAY = 60, 60, 60
LIGHT_GRAY = 120, 120, 120
SNOW_WHITE = 142, 163, 177
STORY_TEXT_WHITE = 235, 250, 247
WHITE = 255, 255, 255

LESS_RED = 211, 70, 70
BROWNISH = 145, 92, 34

ORANGE = 255, 80, 40
YELLOW = 255, 255, 0
BROWN = 200, 100, 0

CYAN = 37, 187, 243

COLOR_SPRING = 93, 150, 60
COLOR_SUMMER = 72, 159, 51
COLOR_AUTUMN = 128, 149, 62
COLOR_WINTER = 210, 219, 221

SEASONS_COLORS = {
    SEASON_SPRING: COLOR_SPRING,
    SEASON_SUMMER: COLOR_SUMMER,
    SEASON_AUTUMN: COLOR_AUTUMN,
    SEASON_WINTER: COLOR_WINTER
}