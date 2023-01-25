import pygame as pg

from utils.colors import *
from utils.functions import position_from_screen, position_to_screen
from utils.display import SCALE
from utils.identifiers import *


class Camera:

    def __init__(self, game):
        self.game = game
        self.box = self.screen.get_rect()
        
    @property
    def screen(self):
        return self.game.screen

    @property
    def world(self):
        return self.game.world

    @property
    def player(self):
        return self.game.player
    
    @property
    def texture_container(self):
        return self.game.texture_container

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
    
    @property
    def debug_mode(self):
        return self.game.debug_mode
    
    @property
    def render_shadows(self):
        return self.game.render_shadows

    def is_on_camera(self, obj):
        return obj.rect.colliderect(self.box)

    def run_debug(self):
        if not self.debug_mode:
            return

        pg.draw.circle(self.screen, BLACK, position_to_screen(self.player.position, self.topleft), 2)
    
    def render_entity(self, entity):
        entity_position_to_screen = position_to_screen(entity.position, self.topleft)
        rect = entity.rect.copy()
        rect.midbottom = entity_position_to_screen

        if entity.in_family("player"):
            rect.bottom += 1*SCALE
            
        entity.draw(self.screen, rect)

        if not self.debug_mode:
            return
        
        # Draw rect of entity
        pg.draw.rect(self.screen, BLUE, rect, 1)
        
        # Draw box of entity
        box_rect = entity.box.copy()
        box_rect.center = position_to_screen(box_rect.center, self.topleft)
        pg.draw.rect(self.screen, BLACK, box_rect, 1)

        # Draw reach of entity
        reach_rect = entity.reach.copy()
        reach_rect.center = position_to_screen(reach_rect.center, self.topleft)
        pg.draw.rect(self.screen, RED, reach_rect, 1)
    
    def get_entity_shadow(self, entity):
        entity_id = entity.id
        shadow_id = SHADOW_SUBTYPE + entity_id

        if shadow_id in self.texture_container:
            return self.texture_container.get(shadow_id)

        elif entity.in_family("small"):
            return self.texture_container["shadows"][SHADOW_SMALL]

        elif entity.in_family("large"):
            return self.texture_container["shadows"][SHADOW_MEDIUM]

        elif entity.in_family("item"):
            return self.texture_container["shadows"][SHADOW_ITEM]

        elif entity.in_family("plant"):
            return self.texture_container["shadows"][SHADOW_PLANT]

        else:
            return

    def draw_shadows(self):
        for entity in self.scene:
            shadow = self.get_entity_shadow(entity)
            
            if not shadow:
                continue
            
            entity_position_to_screen = position_to_screen(entity.position, self.topleft)
            rect = shadow.get_rect(center=entity_position_to_screen)
            self.screen.blit(shadow, rect)
        
    def draw(self):
        if self.render_shadows:
            self.draw_shadows()

        for entity in self.scene:
            self.render_entity(entity)

    def run(self, position):
        self.box.center = position