import pygame as pg

from utils.texts import *
from utils.functions import screen_print
from utils.display import *
from utils.colors import *



MAIN_MENU = 1
SETTINGS = 2
PAUSE_MENU = 3
OFF = 0


class Menu:

    def __init__(self, game):
        self.game = game
        self.running = MAIN_MENU
    
    @property
    def lang(self):
        return self.game.gui.lang
    
    def switch_pause(self):
        self.running = PAUSE_MENU if not self.running else OFF
        self.game.gui.set_prompt_text()
    
    def switch_language(self):
        i = LANGUAGES.index(self.lang)
        n = len(LANGUAGES)
        self.game.gui.set_language( LANGUAGES[ (i+1) % n ] )

        lang = self.lang
        settings_texts = TEXTS[lang]["menu"]["settings"]
        self.game.gui.set_prompt_text(
            settings_texts["lang_changed"].format(lang=lang) )
    
    def set_run(self, value):
        self.running = value
    
    def draw_main_menu(self, screen):
        title_font = self.game.texture_container.title_font
        font = self.game.texture_container.story_font
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        y = 50*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","title"), title_font, (WHITE, SLIGHTLY_LESS_BLACK), (40*SCALE, 5*SCALE), 12, center=(x, y) )

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 15*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",0), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] - 0*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",1), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 15*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",2), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 30*SCALE
        screen_print( screen, get_text(self.lang,"menu","main","buttons",3), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )

    def draw_settings(self, screen):
        font = self.game.texture_container.story_font
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 20*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",0), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] - 5*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",1), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 10*SCALE
        screen_print( screen, get_text(self.lang,"menu","settings","buttons",2), font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )

    def draw_pause_menu(self, screen):
        font = self.game.texture_container.story_font
        x = SCREEN_CENTER[0]

        font.set_bold(False)
        y = SCREEN_CENTER[1] + 10*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","title"), font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, center=(x, y) )
        
        x = 5*SCALE
        y = SCREEN_H - 30*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",0), font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, topleft=(x, y) )
        y = SCREEN_H - 20*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",1), font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, topleft=(x, y) )
        y = SCREEN_H - 10*SCALE
        screen_print( screen, get_text(self.lang,"menu","paused","buttons",2), font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, topleft=(x, y) )

    def draw(self, screen):
        if self.running == MAIN_MENU:
            self.draw_main_menu(screen)
        elif self.running == SETTINGS:
            self.draw_settings(screen)
        elif self.running == PAUSE_MENU:
            self.draw_pause_menu(screen)
        else:
            pass

        self.game.gui.print_prompt()
                    
    def run_main_menu(self, events):
        lang = self.game.gui.lang
        
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_c:
                    self.game.gui.set_prompt_text(
                        get_text(lang,"menu","main","loading_save") )
                    self.game.load_save()
                    self.set_run(OFF)
                elif ev.key == pg.K_n:
                    self.game.gui.set_prompt_text(
                        get_text(lang,"menu","main","loading_new") )
                    self.game.load_new()
                    self.set_run(OFF)
                elif ev.key == pg.K_s:
                    self.set_run(SETTINGS)
                elif ev.key == pg.K_q:
                    self.game.quit()
    
    def run_settings(self, events):
        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE or ev.key == pg.K_s:
                    self.set_run(MAIN_MENU)
                elif ev.key == pg.K_l:
                    self.switch_language()

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

    def run(self, events):
        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()
            elif ev.type == pg.MOUSEBUTTONDOWN:
                print(ev.pos)

        if self.running == MAIN_MENU:
            self.run_main_menu(events)
        elif self.running == SETTINGS:
            self.run_settings(events)
        elif self.running == PAUSE_MENU:
            self.run_pause_menu(events)
        else:
            pass
        
        