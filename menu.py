import pygame as pg

from utils.texts import *
from utils.functions import screen_print
from utils.display import *
from utils.colors import *



MAIN_MENU = 1
WORLDS = 2
SETTINGS = 3
PAUSE_MENU = 4
OFF = 0


class Menu:

    def __init__(self, game):
        self.game = game
        self.running = MAIN_MENU
    
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

    def draw(self, screen):
        if self.running == MAIN_MENU:
            self.draw_main_menu(screen)
        elif self.running == WORLDS:
            self.draw_worlds(screen)
        elif self.running == SETTINGS:
            self.draw_settings(screen)
        elif self.running == PAUSE_MENU:
            self.draw_pause_menu(screen)
        else:
            pass

        self.game.gui.print_prompt()
                    
    def run_main_menu(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_c:
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","main","loading_save") )
                    self.game.load_save()
                    self.set_run(OFF)
                elif ev.key == pg.K_n:
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","main","loading_new") )
                    self.game.load_new()
                    self.set_run(OFF)
                elif ev.key == pg.K_w:
                    self.set_run(WORLDS)
                elif ev.key == pg.K_s:
                    self.set_run(SETTINGS)
                elif ev.key == pg.K_q:
                    self.game.quit()
    
    def run_worlds(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.set_run(MAIN_MENU)
                elif ev.key == pg.K_RETURN:
                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","worlds","load")
                    )
                    self.game.load_save()
                    self.set_run(OFF)
                elif ev.key == pg.K_UP:
                    n = len(self.game.worlds)
                    if n == 0: continue
                    i = max( 0, self.game.world_index - 1 )
                    if i == self.game.world_index: continue
                    self.game.set_world_index(i)
                elif ev.key == pg.K_DOWN:
                    n = len(self.game.worlds)
                    if n == 0: continue
                    i = min( n-1, self.game.world_index + 1 )
                    if i == self.game.world_index: continue
                    self.game.set_world_index(i)
                elif ev.key == pg.K_DELETE:
                    if len(self.worlds) == 0:
                        continue

                    self.game.gui.set_prompt_text(
                        get_text(self.lang,"menu","worlds","delete").format(world=self.game.world_name)
                    )
                    self.game.delete_world()
    
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

    def run(self, events):
        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()
            elif ev.type == pg.MOUSEBUTTONDOWN:
                print(ev.pos)

        if self.running == MAIN_MENU:
            self.run_main_menu(events)
        elif self.running == WORLDS:
            self.run_worlds(events)
        elif self.running == SETTINGS:
            self.run_settings(events)
        elif self.running == PAUSE_MENU:
            self.run_pause_menu(events)
        else:
            pass
        
        