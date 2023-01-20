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
    
    def switch_main(self):
        self.running = MAIN_MENU if not self.running else OFF
    
    def switch_pause(self):
        self.running = PAUSE_MENU if not self.running else OFF
        self.game.gui.set_prompt_text()
    
    def set_run(self, value):
        self.running = value
    
    def draw_main_menu(self, screen):
        title_font = self.game.texture_container.title_font
        font = self.game.texture_container.story_font
        main_menu_texts = TEXTS[self.game.gui.lang]["menu"]["main"]
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        y = 50*SCALE
        screen_print( screen, main_menu_texts["title"], title_font, (WHITE, SLIGHTLY_LESS_BLACK), (40*SCALE, 5*SCALE), 12, center=(x, y) )

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 15*SCALE
        screen_print( screen, main_menu_texts["buttons"][0], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] - 0*SCALE
        screen_print( screen, main_menu_texts["buttons"][1], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 15*SCALE
        screen_print( screen, main_menu_texts["buttons"][2], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 30*SCALE
        screen_print( screen, main_menu_texts["buttons"][3], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )

    def draw_settings(self, screen):
        font = self.game.texture_container.story_font
        settings_texts = TEXTS[self.game.gui.lang]["menu"]["settings"]
        x = SCREEN_CENTER[0]

        screen.fill(BLACK)

        font.set_bold(False)
        y = SCREEN_CENTER[1] - 20*SCALE
        screen_print( screen, settings_texts["buttons"][0], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] - 5*SCALE
        screen_print( screen, settings_texts["buttons"][1], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )
        y = SCREEN_CENTER[1] + 10*SCALE
        screen_print( screen, settings_texts["buttons"][2], font, (WHITE, SLIGHTLY_LESS_BLACK), (5*SCALE, 6*SCALE), 4, center=(x, y) )

    def draw_pause_menu(self, screen):
        font = self.game.texture_container.story_font
        font.set_bold(True)
        position = SCREEN_CENTER[0], SCREEN_H - 21*SCALE

        screen_print( screen, "Paused", font, (WHITE, SLIGHTLY_LESS_BLACK), (10, 6), 2, center=position )
        font.set_bold(False)
        position = SCREEN_CENTER[0], SCREEN_H - 10*SCALE
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

        self.game.gui.print_prompt()
                    
    def run_main_menu(self, events):
        lang = self.game.gui.lang
        main_menu_texts = TEXTS[lang]["menu"]["settings"]

        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                print(ev.pos)
            
            elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_c:
                        self.game.gui.set_prompt_text("Loading saved world...")
                        self.game.load_save()
                        self.switch_main()

                    elif ev.key == pg.K_n:
                        self.game.gui.set_prompt_text("Generating new world...")
                        self.game.load_new()
                        self.switch_main()
                    
                    elif ev.key == pg.K_s:
                        self.set_run(SETTINGS)
                    
                    elif ev.key == pg.K_q:
                        self.game.quit()
                    
                    else:
                        pass
    
    def run_settings(self, events):
        for ev in events:
            if ev.type == pg.QUIT:
                self.game.quit()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                print(ev.pos)
            
            elif ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE or ev.key == pg.K_s:
                        self.set_run(MAIN_MENU)
                    
                    elif ev.key == pg.K_l:
                        self.game.gui.switch_language()
                        lang = self.game.gui.lang
                        settings_texts = TEXTS[lang]["menu"]["settings"]
                        self.game.gui.set_prompt_text(
                            settings_texts["lang_changed"].format(lang=lang) )
                    
                    else:
                        pass

    def run_pause_menu(self, events):
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
        
        