import pygame as pg
from settings import *
from textures import *
from player import *
from world import *
from camera import *
from inventory import *


class MainGame:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_RES, flags = 0)
        pg.display.set_caption(SCREEN_CAPTION)
        self.clock = pg.time.Clock()

        self.running = False
        self.show_fps = True
        self.debug_mode = False

        self.texture_container = TextureContainer()

        self.world = World(self)
        self.camera = Camera(self)
        self.inventory = Inventory(self)
        
        self.setup_player()
        
        print("Init successful.")

    @property
    def debug_font(self):
        return self.texture_container.debug_font

    def setup_player(self):
        player_texture = self.texture_container.players[PLAYER0]
        self.player = Player(player_texture, (0, 0), self)

        self.inventory.add(AXE, 1)

        self.world.add_child(self.player)

    def get_fps(self):
        if not self.show_fps:
            return

        fps = round( self.clock.get_fps() )
        print_( self.screen, fps, self.debug_font, WHITE, BLACK, topleft=(0, 0) )
        
    def get_debug(self):
        if not self.debug_mode:
            return
        
        center = SCREEN_CENTER
        pg.draw.circle(self.screen, BLACK, center, 5)

        self.camera.get_debug()

    def get_input(self):
        events = pg.event.get()
        
        for ev in events:
            if ev.type == pg.QUIT:
                self.running = False

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    self.running = False
                    
                elif ev.key == pg.K_f:
                    self.show_fps = not self.show_fps

                elif ev.key == pg.K_r:
                    self.debug_mode = not self.debug_mode

        if not self.inventory.expanded:
            self.player.get_input(events)

        self.inventory.get_input(events)

    def draw(self):
        self.world.draw(self.screen)
        self.camera.draw()
        self.inventory.draw(self.screen)

        if self.player.is_cutting_tree:
            tree = self.player.action_actor
            print_(self.screen, tree.health, self.debug_font, WHITE, BLACK, center = SCREEN_CENTER)

    def run(self):
        print("Now running.")
        self.running = True
        
        while self.running:
            self.get_input()
            
            self.world.run()

            # Keep this after world.run(), bcs there the player position gets updated
            camera_center = self.player.position
            self.camera.run(camera_center)
            
            self.draw()
            
            self.get_fps()
            self.get_debug()
            
            pg.display.update()
            self.clock.tick(FPS)

        self.quit()

    def quit(self):
        print("Quitting.")
        self.running = False
        pg.quit()


if __name__ == "__main__":
    MainGame().run()
