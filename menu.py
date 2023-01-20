import pygame as pg

import utils.texts as texts
import utils.display as display
from utils.colors import *
from utils.functions import screen_print


MAIN_MENU = 1
SETTINGS = 2
PAUSE_MENU = 3
OFF = 0


class Menu:

    def __init__(self, game):
        self.game = game

        self.language = texts.EN
        self.running = MAIN_MENU
    
    def switch_main(self):
        self.running = MAIN_MENU if not self.running else OFF
    
    def switch_pause(self):
        if self.running and self.running != PAUSE_MENU:
            return

        self.running = PAUSE_MENU if not self.running else OFF
        self.game.gui.set_prompt_text()
    
    def set_run(self, value):
        self.running = value
    
    def draw_main_menu(self, screen):
        screen.fill(BLACK)
        self.game.gui.print_prompt()

    def draw_settings(self, screen):
        pass

    def draw_pause_menu(self, screen):
        font = self.game.texture_container.story_font
        font.set_bold(True)
        position = display.SCREEN_CENTER[0], display.SCREEN_H - 21*display.SCALE

        screen_print( screen, "Paused", font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, center=position )
        font.set_bold(False)
        position = display.SCREEN_CENTER[0], display.SCREEN_H - 10*display.SCALE
        screen_print( screen, "Press ESC to resume, Q to quit or M to return to menu.", font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, center=position )

    def draw(self, screen):
        if self.running == MAIN_MENU:
            self.draw_main_menu(screen)
        elif self.running == SETTINGS:
            self.draw_settings(screen)
        elif self.running == PAUSE_MENU:
            self.draw_pause_menu(screen)
        else:
            pass
                    
    def run_main_menu(self, events):
        self.game.gui.set_prompt_text("Load saved world? y/n")

        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                print("Click!")
            
            elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_y:
                        self.game.gui.set_prompt_text("Loading saved world...")
                        self.game.load_save()
                        self.switch_main()

                    elif ev.key == pg.K_n:
                        self.game.gui.set_prompt_text("Generating new world...")
                        self.game.load_new()
                        self.switch_main()
                    
                    else:
                        pass
    
    def run_settings(self, events):
        pass

    def run_pause_menu(self, events):
        self.game.gui.set_prompt_text("Paused.")

        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                print(ev.pos)
            
            elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        self.switch_pause()
                    
                    elif ev.key == pg.K_q:
                        self.game.quit()
                    
                    elif ev.key == pg.K_m:
                        self.set_run(MAIN_MENU)
                        self.game.clean()
                    
                    else:
                        pass

    def run(self, events):
        if self.running == MAIN_MENU:
            self.run_main_menu(events)
        elif self.running == SETTINGS:
            self.run_settings(events)
        elif self.running == PAUSE_MENU:
            self.run_pause_menu(events)
        else:
            pass
        
        