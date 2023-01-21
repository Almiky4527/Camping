try:
    from .display import SCALE
except ImportError:
    from display import SCALE

from pygame import Surface, Rect


DEFAULT_BOX_SIZE = (16, 8)


class BaseEntity:

    def __init__(self, image : Surface, position, parent):
        self.image = image
        self.rect = self.image.get_rect(midbottom=position)
        
        self.box = Rect( (0, 0), (0, 0) )
        # Cannot use self.set_position, it will be called from the higher class.
        self.box.midbottom = position

        self.parent = parent
        
    @property
    def position(self):
        return self.rect.midbottom
    
    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]

    def set_position(self, position):
        x, y = position
        self.rect.midbottom = x, y
        self.box.midbottom = x, y + SCALE
    
    def set_x(self, value):
        y = self.position[1]
        self.set_position( (value, y) )
    
    def set_y(self, value):
        x = self.position[0]
        self.set_position( (x, value) )
    
    def collision(self, entity):
        return entity.box.colliderect(self.box)
    
    def set_box_right(self, value):
        x = value - (self.box.width / 2)
        self.set_x(x)
    
    def set_box_left(self, value):
        x = value + (self.box.width / 2)
        self.set_x(x)
    
    def set_box_top(self, value):
        y = value + (self.box.height - SCALE)
        self.set_y(y)
    
    def set_box_bottom(self, value):
        y = value - SCALE
        self.set_y(y)
        
    def draw(self, screen : Surface, rect : Rect):
        screen.blit(self.image, rect)

    def update(self):
        pass


# === ERRORS / EXCEPTIONS ===


class ContainerFull (Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TextureTypeError (TypeError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CannotSpawnHere (Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class LanguageError (TypeError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)