import pygame as pg

from saving import *
from menu import *
from textures import *
from player import *
from entities import *
from world import *
from camera import *
from gui import *
from inventory import *

from utils.texts import *


class MainGame:

    def __init__(self):
        self.setup_pygame()
        self.setup_main_game()
        print("Init successful.")

    @property
    def debug_font(self):
        return self.texture_container.debug_font
    
    def setup_pygame(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_RES, flags = 0)
        pg.display.set_caption(SCREEN_CAPTION)
        self.clock = pg.time.Clock()

    def setup_main_game(self):
        self.running = False
        self.debug_mode = False

        self.texture_container = TextureContainer()
        self.saveloadstream = SaveLoadStream(self)
        self.menu = Menu(self)
        self.gui = GUI(self)
        self.camera = Camera(self)

    def setup_world(self):
        self.world = World(self)
        self.world.generate()

    def setup_inventory(self):
        self.inventory = Inventory( [ {} for _ in range(9) ], self )

        STARTING_ITEMS = [
            [ITEM_AXE],
            [ITEM_TENT],
            [ITEM_MATCHES, 32]
        ]

        for item_data_and_count in STARTING_ITEMS:
            self.inventory.add( item( *item_data_and_count ) )

    def setup_player(self):
        player_texture_set = self.texture_container["JohnDoe"]
        
        self.player = Player(
            self,
            player_texture_set,
            data=entity(ENTITY_PLAYER),
            position=(0, 0),
            parent=self.world
        )

        self.player.set_saturation(50)
        
        self.world.add_child(self.player)

    def run_debug(self):
        if not self.debug_mode:
            return

        self.camera.run_debug()
        self.gui.run_debug()

    def get_input(self, events):
        for ev in events:
            if ev.type == pg.QUIT:
                self.running = False

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.menu.switch_pause()
                    
                elif ev.key == pg.K_r:
                    self.debug_mode = not self.debug_mode
        
        self.gui.get_input(events)

        if not self.inventory.expanded:
            self.player.get_input(events)

        self.inventory.get_input(events)

    def draw(self):
        self.world.draw(self.screen)
        self.camera.draw()
        self.gui.draw()
    
    def display_update(self):
        pg.display.update()
        self.clock.tick(FPS)
    
    def run(self):
        print("Now running.")
        self.running = True

        # Main loop.
        while self.running:
            events = pg.event.get()

            if self.menu.running:
                self.menu.run(events)
                self.menu.draw(self.screen)

            else:
                self.world.run()
                self.camera.run(self.player.position)

                self.get_input(events)

                self.draw()
                
                self.run_debug()
            
            self.gui.run()

            self.display_update()

        # Quit pygame.
        pg.quit()
    
    def load_new(self):
        self.setup_world()
        self.setup_player()
        self.setup_inventory()
    
    def load_save(self):
        err_while_loading = self.saveloadstream.load()

        if err_while_loading:
            # Infinite while loop... Temporary so the game wont break.
            # IMPLEMENT HANDLING FOR ERRORS WHILE LOADING SAVE FILES.
            while True: pass
    
    def save(self):
        self.gui.set_prompt_text("Do you want to save? y/n")

        if self.gui.prompt_input_buffer == pg.K_y:
            if self.inventory.expanded:
                self.inventory.toggle_expand()

            self.saveloadstream.save()
            self.gui.set_prompt_text("Game state saved.")
            self.player.stop_action()
        
        elif self.gui.prompt_input_buffer == pg.K_n:
            self.gui.set_prompt_text("Canceled.")
            self.player.stop_action()
        
    # Program is increasing on RAM when reloading game from menu.
    def clean(self):
        del self.world
        del self.player
        del self.inventory

    def quit(self):
        print("Quitting.")
        self.running = False


if __name__ == "__main__":
    MainGame().run()
