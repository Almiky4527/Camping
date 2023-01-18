try:
    from .colors import *
except ImportError:
    from colors import *

from pygame import draw
from pygame import Rect, Surface, image, transform
from pygame.time import Clock
from pygame.math import Vector2


# --- Camera Coordiante System <-> In-Game Coordinate System ---

def position_from_screen(position, camera_topleft):
    '''Translates position given in 'screen' coordinates to position in 'in-game' coordinates.'''
    x1, y1 = position
    x2, y2 = camera_topleft
    return ( (x1 + x2), (y1 + y2) )

def position_to_screen(position, camera_topleft):
    '''Translates position given in 'in-game' coordinates to position in 'screen' coordinates.'''
    x1, y1 = position
    x2, y2 = camera_topleft
    return ( (x1 - x2), (y1 - y2) )

# --------------------------------------------------------------


# --- Stringify FPS ---
def fps_str(clock : Clock):
    return f"{ round( clock.get_fps() ) }"
# ---------------------


# --- Hepful functions for TextureContainer ---

def scale_(surface : Surface, scale : float):
    w, h = surface.get_size()
    new_size = ( w * scale, h * scale )
    return transform.scale(surface, new_size)

def cropp_(surface : Surface, rect : Rect):
    if type(rect) != Rect:
        raise TypeError("arg 'rect' (2) must be of type pygame.Rect")

    return surface.subsurface(rect)

def make_texture(img, scale=None, rect=None, colorkey=BLACK):
    if type(img) == str:
        img = image.load(img)
    elif type(img) != Surface:
        raise TypeError("arg 'img' (1) must be either of type str (path to file) or pygame.Surface")

    img = img.convert()

    if rect:
        img = cropp_(img, rect)
    if colorkey:
        img.set_colorkey(colorkey)
    if scale:
        img = scale_(img, scale)
        
    return img

# ---------------------------------------------


def directionalize(vector : Vector2):
    '''Turns any pygame.math.Vector2 into a vector representing direction for movement of entities (only values of 1, 0, -1 for each axis).'''
    v = vector.copy()
    v.x = 1 if v.x > 0 else -1 if v.x < 0 else 0
    v.y = 1 if v.y > 0 else -1 if v.y < 0 else 0
    return v


def screen_print(surface, text, font, colors=(WHITE, None), inflation=(0, 0), br=0, opacity=255, topleft=None, center=None):
    if not topleft and not center:
        raise TypeError("position must be provided ('topleft' or 'center')")
    
    fg, bg = colors
    render_text = font.render( str(text), True, fg )
    rect = render_text.get_rect()

    if topleft:
        rect.topleft = topleft
    elif center:
        rect.center = center
    
    if bg:
        
        rect2 = rect.inflate(inflation[0], inflation[1])
        base_surf = Surface( (rect2.w, rect2.h) )
        base_surf.set_colorkey(BLACK)
        draw.rect(base_surf, bg, (0, 0, rect2.w, rect2.h), border_radius=br)
        base_surf.set_alpha(opacity)
        surface.blit(base_surf, rect2)
        
        # rect2 = rect.inflate(inflation[0], inflation[1])
        # draw.rect(surface, bg, rect2, border_radius=br)
        
    render_text.set_alpha(opacity)
    surface.blit(render_text, rect)


def make_grid(rect : Rect, positions):
    positions_x, positions_y = positions
    step_x, step_y = rect.w // positions_x, rect.h // positions_y

    range_x = range(rect.left, rect.right + 1, step_x)
    range_y = range(rect.top, rect.bottom + 1, step_y)

    return range_x, range_y
