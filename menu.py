import pygame as pg
from random import choice

from utils.texts import *
from utils.functions import screen_print, scale_
from utils.display import *
from utils.colors import *



MAIN_MENU = 1
WORLDS = 2
SETTINGS = 3
PAUSE_MENU = 4
NEW_DAY_LOADING = 5
SELECT_CHARACTER = 6
OFF = 0


class Menu:

    def __init__(self, game):
        self.game = game
        self.running = MAIN_MENU

        self.new_day_timer = 0
        self.new_day_random_tip = ""
    
    @property
    def lang(self):
        return self.game.lang
    
    @property
    def story_font(self):
        return self.game.texture_container.story_font
    
    @property
    def title_font(self):
        return self.game.texture_container.title_font
    
    @property
    def text_specs_1(self):
        return self.story_font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4
    
    @property
    def text_specs_1_locked(self):
        return self.story_font, (GRAY, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4
    
    @property
    def text_specs_2(self):
        return self.title_font, (WHITE, SLIGHTLY_LESS_BLACK), (40*SCALE, 5*SCALE), 12
    
    @property
    def text_specs_3(self):
        return self.story_font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 2*SCALE), 4
    
    @property
    def worlds(self):
        return self.game.worlds
    
    def switch_pause(self):
        self.running = PAUSE_MENU if not self.running else OFF
        self.game.gui.set_prompt_text()
    
    def switch_language(self):
        i = LANGUAGES.index(self.lang)
        n = len(LANGUAGES)
        self.game.set_language( LANGUAGES[ (i+1) % n ] )

        lang = self.lang
        settings_texts = TEXTS[lang]["menu"]["settings"]
        self.game.gui.set_prompt_text(
            settings_texts["lang_changed"].format(lang=lang) )
    
    def set_run(self, value):
        self.running = value
    
    def draw_main_menu(self, screen):
        font = self.game.texture_container.story_font
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        y = 50*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","title"), *self.text_specs_2, center=(x, y) )

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 15*SCALE

        if len(self.worlds) == 0:
            screen_print( screen, get_text(self.lang,"menu","main","buttons",0), *self.text_specs_1_locked, center=(x, y) )
        else:
            screen_print( screen, get_text(self.lang,"menu","main","buttons",0), *self.text_specs_1, center=(x, y) )

        y = SCREEN_CENTER[1] - 0*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",1), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 15*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",2), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 30*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",3), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 45*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",4), *self.text_specs_1, center=(x, y) )

    def draw_worlds(self, screen):
        x = SCREEN_CENTER[0] - 80*SCALE

        screen.fill(BLACK)

        y = SCREEN_CENTER[1] - 22.5*SCALE
        screen_print( screen, get_text(self.lang,"menu","worlds","buttons",0), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] - 7.5*SCALE
        screen_print( screen, get_text(self.lang,"menu","worlds","buttons",1), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 7.5*SCALE
        screen_print( screen, get_text(self.lang,"menu","worlds","buttons",2), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 22.5*SCALE
        screen_print( screen, get_text(self.lang,"menu","worlds","buttons",3), *self.text_specs_1, center=(x, y) )

        x = SCREEN_CENTER[0] + 0*SCALE
        y = SCREEN_CENTER[1]
        screen_print( screen, ">", *self.text_specs_1, center=(x, y) )

        x = SCREEN_CENTER[0] + 21*SCALE
        screen_print( screen, self.game.world_name, *self.text_specs_1, center=(x, y) )

    def draw_settings(self, screen):
        font = self.story_font
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 20*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",0), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] - 5*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",1), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 10*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",2), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 25*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",3), *self.text_specs_1, center=(x, y) )
        y = SCREEN_CENTER[1] + 40*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",4), *self.text_specs_1, center=(x, y) )

    def draw_pause_menu(self, screen):
        font = self.story_font
        x = SCREEN_CENTER[0]

        font.set_bold(False)
        y = SCREEN_CENTER[1] + 10*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","title"), *self.text_specs_3, center=(x, y) )
        
        x = 5*SCALE
        y = SCREEN_CENTER[1] - 15*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",0), *self.text_specs_3, topleft=(x, y) )
        y = SCREEN_CENTER[1] - 5*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",1), *self.text_specs_3, topleft=(x, y) )
        y = SCREEN_CENTER[1] + 5*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",2), *self.text_specs_3, topleft=(x, y) )
        y = SCREEN_CENTER[1] + 15*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",3), *self.text_specs_3, topleft=(x, y) )

    def draw_new_day_loading(self, screen):
        font = self.story_font
        font.set_bold(False)

        screen.fill(BLACK)

        x, y = SCREEN_CENTER[0], SCREEN_H - 40*SCALE
        w, h = SCREEN_W - (5*2)*SCALE, 10*SCALE
        progress_bar_rect = pg.Rect(0, 0, w, h)
        progress_bar_rect.center = (x, y)
        self.game.gui.draw_progress_bar( progress_bar_rect, self.new_day_timer, colors=(SLIGHTLY_LESS_BLACK, WHITE) )

        screen_print( screen, self.new_day_random_tip, *self.text_specs_3, center=(x, y + 20*SCALE) )

        if self.new_day_timer >= 100:
            screen_print( screen, get_text(self.lang,"menu","new_day_loading","continue"), *self.text_specs_1, center=(x, y - 25*SCALE) )
    
    def draw_select_character(self, screen):
        font = self.story_font
        font.set_bold(False)

        texture_container = self.game.texture_container

        screen.fill(BLACK)
        x, y = SCREEN_CENTER[0], SCREEN_CENTER[1] - 50*SCALE
        screen_print( screen, get_text(self.lang, "menu", "select_character", "title"), *self.text_specs_2, center=(x, y) )
        
        y = y + 100*SCALE
        x = SCREEN_CENTER[0] - 30*SCALE
        screen_print( screen, '1', *self.text_specs_2, center=(x, y) )
        char_1_texture = scale_( texture_container["JohnDoe"][0][0], 2 )
        rect = char_1_texture.get_rect( midbottom=(x, y - 10*SCALE) )
        screen.blit(char_1_texture, rect)

        x = SCREEN_CENTER[0] + 30*SCALE
        screen_print( screen, '2', *self.text_specs_2, center=(x, y) )
        char_2_texture = scale_( texture_container["JaneSmith"][0][0], 2 )
        rect = char_1_texture.get_rect( midbottom=(x, y - 10*SCALE) )
        screen.blit(char_2_texture, rect)

    def draw(self, screen):
        if self.running == MAIN_MENU:
            self.draw_main_menu(screen)
        elif self.running == WORLDS:
            self.draw_worlds(screen)
        elif self.running == SETTINGS:
            self.draw_settings(screen)
        elif self.running == PAUSE_MENU:
            self.draw_pause_menu(screen)
        elif self.running == NEW_DAY_LOADING:
            self.draw_new_day_loading(screen)
        elif self.running == SELECT_CHARACTER:
            self.draw_select_character(screen)
        else:
            pass

        self.game.gui.print_prompt()
                    
    def run_main_menu(self, events):
        def _load_last_world():
            if len(self.worlds) == 0:
                return

            self.game.gui.set_prompt_text(
                get_text(self.lang, "menu", "main", "loading_save")
            )
            self.game.load_save()
            self.set_run(OFF)

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_c:
                    _load_last_world()
                elif ev.key == pg.K_n:
                    self.set_run(SELECT_CHARACTER)
                elif ev.key == pg.K_w:
                    self.set_run(WORLDS)
                elif ev.key == pg.K_s:
                    self.set_run(SETTINGS)
                elif ev.key == pg.K_q:
                    self.game.quit()
    
    def run_worlds(self, events):
        def _run_world():
            if len(self.worlds) == 0:
                self.set_run(SELECT_CHARACTER)
                return

            self.game.gui.set_prompt_text(
                get_text(self.lang, "menu", "worlds", "load")
            )
            self.game.load_save()
            self.set_run(OFF)
        
        def _scroll_worlds(dif):
            n = len(self.worlds)
            if n == 0:
                return

            i = min( max( 0, self.game.world_index+dif ), n-1 )
            if i == self.game.world_index:
                return

            self.game.set_world_index(i)
        
        def _del_world():
            if len(self.worlds) == 0:
                return

            self.game.gui.set_prompt_text(
                get_text(self.lang, "menu", "worlds", "delete").format(world=self.game.world_name)
            )
            self.game.delete_world()

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.set_run(MAIN_MENU)
                elif ev.key == pg.K_RETURN:
                    _run_world()
                elif ev.key == pg.K_UP:
                    _scroll_worlds(-1)
                elif ev.key == pg.K_DOWN:
                    _scroll_worlds(+1)
                elif ev.key == pg.K_DELETE:
                    _del_world()
    
    def run_settings(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.set_run(MAIN_MENU)
                elif ev.key == pg.K_l:
                    self.switch_language()
                elif ev.key == pg.K_f:
                    self.game.set_fullscreen_mode(not self.game.fullscreen_mode)
                    i = int(self.game.fullscreen_mode)
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","settings","fullscreen",i)
                    )
                elif ev.key == pg.K_d:
                    self.game.set_debug_mode(not self.game.debug_mode)
                    i = int(self.game.debug_mode)
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","settings","debug",i)
                    )
                elif ev.key == pg.K_s:
                    self.game.set_render_shadows(not self.game.render_shadows)
                    i = int(self.game.render_shadows)
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","settings","shadows",i)
                    )

    def run_pause_menu(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.switch_pause()
                elif ev.key == pg.K_q:
                    self.game.quit()
                elif ev.key == pg.K_m:
                    self.set_run(MAIN_MENU)
                    self.game.clean()
                elif ev.key == pg.K_d:
                    self.game.set_debug_mode(not self.game.debug_mode)
                    i = int(self.game.debug_mode)
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","settings","debug",i)
                    )

    def run_new_day_loading(self, events):
        if self.new_day_timer == 0:
            self.new_day_random_tip = choice( TEXTS[self.lang]["menu"]["new_day_loading"]["tips"] )
            
            # Skip to the next day
            self.game.world.next_day()
            self.game.saveloadstream.save(self.game.world_name)

        if self.new_day_timer < 100:
            self.new_day_timer += 10/FPS

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if not self.new_day_timer >= 100:
                    continue
                
                self.new_day_timer = 0
                self.set_run(OFF)
    
    def run_select_character(self, events):
        selected_character_name = ""

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_1:
                    selected_character_name = "JohnDoe"
                elif ev.key == pg.K_2:
                    selected_character_name = "JaneSmith"
                else:
                    continue

                self.game.gui.set_prompt_text(
                    get_text(self.lang, "menu", "main", "loading_new")
                )
                self.game.load_new(player_name=selected_character_name)
                self.set_run(OFF)

    def run(self, events):
        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()

        if self.running == MAIN_MENU:
            self.run_main_menu(events)
        elif self.running == WORLDS:
            self.run_worlds(events)
        elif self.running == SETTINGS:
            self.run_settings(events)
        elif self.running == PAUSE_MENU:
            self.run_pause_menu(events)
        elif self.running == NEW_DAY_LOADING:
            self.run_new_day_loading(events)
        elif self.running == SELECT_CHARACTER:
            self.run_select_character(events)
        else:
            pass
        
        