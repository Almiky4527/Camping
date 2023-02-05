import pygame as pg

from utils.display import *
from utils.colors import *
from utils.functions import *
from utils.texts import *
from utils.classes import LanguageError


PROMPT_DURATION = 5 * FPS


class GUI:

    def __init__(self, game):
        self.game = game

        self.prompt_text = ""
        self.prompt_time = 0
        self.prompt_input_buffer = 0

    @property
    def lang(self):
        return self.game.lang
    
    @property
    def screen(self):
        return self.game.screen
    
    @property
    def clock(self):
        return self.game.clock
    
    @property
    def texture_container(self):
        return self.game.texture_container
    
    @property
    def debug_font(self):
        return self.game.debug_font

    @property
    def player(self):
        return self.game.player

    @property
    def inventory(self):
        return self.game.inventory
    
    @property
    def debug_mode(self):
        return self.game.debug_mode
    
    @property
    def world(self):
        return self.game.world
    
    def set_prompt_text(self, text : str = None):
        if not text:
            text = ""

        self.prompt_text = text
        self.prompt_time = 0
        
    def draw(self):
        # --- Prompt ---
        self.print_prompt()
        # --------------

        if self.game.menu.running:
            return

        # --- Print item info in inventory ---
        if self.inventory.expanded and self.inventory.hover_slot and not self.inventory.dragging_slot:
            x, y = SCREEN_CENTER[0], 620
            self.print_item_name( self.inventory.hover_slot, position=(x, y) )
            self.print_item_legend( self.inventory.hover_slot, position=(x, y+32) )

            # Additional info for debugging.
            if self.debug_mode:
                self.print_item_info(self.inventory.hover_slot)
        # ------------------------------------

        # --- Invenotry ---
        self.inventory.draw(self.screen)
        # -----------------

        # --- Attacking Progress Bar ---
        if self.player.is_attacking:
            target = self.player.target
            rect = pg.Rect(0, 0, 50, 8)
            rect.center = position_to_screen(target.rect.center, self.game.camera.topleft)
            self.draw_progress_bar(rect, target.health, max_value=target.max_health)
        # ------------------------------

        # --- Looting Progress Bar ---
        if self.player.is_looting:
            target = self.player.target
            rect = pg.Rect(0, 0, 50, 8)
            rect.center = position_to_screen(target.rect.center, self.game.camera.topleft)
            self.draw_progress_bar(rect, self.player.action_time, max_value=target.looting_time*FPS)
        # ----------------------------
    
        if self.inventory.expanded:
            # --- World: Days, Season ---
            self.print_world_state()
            # ---------------------------
            return

        # --- Player Health Bar ---
        rect = pg.Rect(100, 16, 100, 16)
        health = round(self.player.health)
        self.draw_progress_bar(rect, health)
        # -------------------------
    
        # --- Player Saturation Bar ---
        rect = pg.Rect(100, 40, 100, 16)
        saturation = round(self.player.saturation)
        self.draw_progress_bar( rect, saturation, colors=(LESS_RED, BROWNISH) )
        # --------------------------

        # --- Player Stamina Bar ---
        rect = pg.Rect(100, 64, 100, 16)
        stamina = round(self.player.stamina)
        self.draw_progress_bar( rect, stamina, colors=(LESS_RED, YELLOW) )
        # --------------------------
    
    def draw_progress_bar( self, rect, value, max_value=100, colors=(LESS_RED, GREEN) ):
        pg.draw.rect(self.screen, colors[0], rect)

        if not max_value:
            pg.draw.rect(self.screen, colors[1], rect)
            return

        value_percentage = value / max_value
        rect.w *= value_percentage
        pg.draw.rect(self.screen, colors[1], rect)
    
    def print_item_name( self, item_data : dict, position=(45, 90), colors=(STORY_TEXT_WHITE, SLIGHTLY_LESS_BLACK) ):
        item_id = item_data["id"]
        text = get_name(item_id, self.lang)
        font = self.texture_container.story_font
        font.set_bold(True)

        screen_print(self.screen, text, font, colors=colors, inflation=(8, 6), br=4, center=position)
    
    def print_item_legend( self, item_data : dict, position=(SCREEN_CENTER[0], 632), colors=(STORY_TEXT_WHITE, SLIGHTLY_LESS_BLACK) ):
        item_id = item_data["id"]
        text = get_legend(item_id, self.lang)
        font = self.texture_container.story_font
        font.set_bold(False)

        screen_print(self.screen, text, font, colors=colors, inflation=(8, 6), br=4, center=position)
    
    def print_item_info( self, item_data : dict, position=(10, 10), colors=(WHITE, SLIGHTLY_LESS_BLACK) ):
        lines = textify_data(item_data)
        font = self.texture_container.inventory_font
        x, y = position
        font_size = font.get_linesize()

        for i, line in enumerate(lines):
            dif = font_size * i
            screen_print( self.screen, line, font, colors=colors, inflation=(4, 4), topleft=(x, y + dif) )

    def print_prompt( self, position=(25, 700), colors=(WHITE, SLIGHTLY_LESS_BLACK) ):
        if not self.prompt_text:
            return

        font = self.texture_container.story_font
        font.set_bold(False)
        opacity = 255 - ( max( 0, self.prompt_time - (PROMPT_DURATION - 120) ) )*2
        screen_print(self.screen, self.prompt_text, font, colors=colors, inflation=(10, 6), br=2, opacity=opacity, topleft=position)
    
    def print_world_state( self, position=(SCREEN_W - 60*SCALE, 5*SCALE) ):
        day = self.world.day + 1
        season_name = get_text(self.lang, "world", self.world.season)
        world_info_text = get_text(self.lang, "world", "info_text").format(season=season_name, day=day)

        font = self.texture_container.story_font
        font.set_bold(False)
        colors = ( WHITE, SLIGHTLY_LESS_BLACK )
        screen_print(self.screen, world_info_text, font, colors=colors, inflation=(10, 6), br=3, topleft=position)

        self.print_world_time()
    
    def print_world_time( self, position=(SCREEN_W - 60*SCALE, 15*SCALE) ):
        font = self.texture_container.story_font
        font.set_bold(False)
        colors = ( WHITE, SLIGHTLY_LESS_BLACK )

        seconds = str( self.world.seconds % 60 )
        minutes = str( self.world.seconds // 60 )
        time_text = f"{ minutes.zfill(2) }:{ seconds.zfill(2) }"

        screen_print(self.screen, time_text, font, colors=colors, inflation=(10, 6), br=3, topleft=position)
    
    def get_input(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                self.prompt_input_buffer = ev.key
    
    def update_prompt(self):
        if self.prompt_text:
            self.prompt_time += 1
        
        if self.prompt_time >= PROMPT_DURATION:
            self.set_prompt_text()
            self.prompt_time = 0
    
    def run_debug(self):
        fps = fps_str(self.clock)
        screen_print(self.screen, fps, self.debug_font, colors=(WHITE, SLIGHTLY_LESS_BLACK), topleft=SCREEN_TOPLEFT)

    def run(self):
        self.update_prompt()