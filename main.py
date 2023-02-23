import pygame as pg
from random import random, randint

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


SETTINGS_DEFAULT = {
    "language": "English",
    "fullscreen": False,
    "debug": False,
    "render_shadows": True,
    
    "world_index": 0,
    "worlds": []
}


class MainGame:

    def __init__(self):
        self.setup_pygame()
        self.setup_main_game()
        print("Init successful.")

    @property
    def debug_font(self):
        return self.texture_container.debug_font
    
    @property
    def lang(self):
        return self.settings["language"]
    
    @property
    def debug_mode(self):
        return self.settings["debug"]

    @property
    def render_shadows(self):
        return self.settings["render_shadows"]
    
    @property
    def fullscreen_mode(self):
        return self.settings["fullscreen"]
    
    @property
    def world_index(self):
        return self.settings["world_index"]
    
    @property
    def world_name(self):
        return self.worlds[self.world_index] if len(self.worlds) != 0 else get_text(self.lang,"menu","worlds","empty")
    
    @property
    def worlds(self):
        return self.settings["worlds"]
    
    def set_language(self, value : str):
        if value not in LANGUAGES:
            LanguageError(f"language '{value}' not found")
        
        self.settings["language"] = value
        self.saveloadstream.write_settings()
    
    def set_debug_mode(self, value : bool):
        self.settings["debug"] = value
        self.saveloadstream.write_settings()
    
    def set_render_shadows(self, value : bool):
        self.settings["render_shadows"] = value
        self.saveloadstream.write_settings()
    
    def set_fullscreen_mode(self, value : bool):
        self.settings["fullscreen"] = value
        pg.display.toggle_fullscreen()
        self.saveloadstream.write_settings()
    
    def set_world_index(self, value : int):
        self.settings["world_index"] = value
        self.saveloadstream.write_settings()
    
    def add_world(self, name : str):
        self.worlds.append(name)
        self.saveloadstream.write_settings()
    
    def remove_world(self, name : str):
        self.worlds.remove(name)
        self.saveloadstream.write_settings()

    def set_settings(self, data : dict):
        self.settings = data
        
    def setup_pygame(self):
        pg.init()
        flags = pg.SCALED
        self.screen = pg.display.set_mode(SCREEN_RES, flags=flags, vsync=1)
        pg.display.set_caption(SCREEN_CAPTION)
        self.clock = pg.time.Clock()

    def setup_main_game(self):
        self.running = False
        self.settings = SETTINGS_DEFAULT
        
        self.texture_container = TextureContainer()
        self.saveloadstream = SaveLoadStream(self)
        self.menu = Menu(self)
        self.gui = GUI(self)
        self.camera = Camera(self)

        self.saveloadstream.load_settings()

        if self.fullscreen_mode:
            pg.display.toggle_fullscreen()

    def setup_world(self):
        self.world = World(self)
        self.world.generate(INITIAL_GENERATION)
        self.world.next_season()

    def setup_inventory(self):
        self.inventory = Inventory( [ {} for _ in range(9) ], self )

        STARTING_ITEMS = [
            [ITEM_AXE],
            [ITEM_TENT],
            [ITEM_MATCHES, 32],
            [ITEM_CABIN_PLAN],
            [ITEM_JACKET],
            [ITEM_HAT]
        ]

        for item_data_and_count in STARTING_ITEMS:
            self.inventory.add( item( *item_data_and_count ) )

    def setup_player(self, name="JohnDoe"):
        player_texture_set = self.texture_container[name]
        
        self.player = Player(
            game=self,
            name=name,
            data=entity(ENTITY_PLAYER),
            image=player_texture_set[SOUTH][0],
            texture_set=player_texture_set,
            position=(0, 0),
            parent=self.world
        )
        
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
    
    def load_new(self, player_name):
        last_world_num = int( self.worlds[-1][6:] ) if len(self.worlds) > 0 else 0
        world_name = f"World {last_world_num+1}"

        self.add_world(world_name)
        self.set_world_index(last_world_num)

        self.setup_world()
        self.setup_player(player_name)
        self.setup_inventory()

        self.saveloadstream.save(world_name)
    
    def load_save(self, world_index=None):
        if world_index:
            self.set_world_index(world_index)

        if len(self.worlds) == 0:
            raise NoWorlds

        else:
            err_while_loading = self.saveloadstream.load(self.world_name)

            if err_while_loading:
                raise WorldLoadingError("unable to find world")
    
    def save(self):
        if not self.world.can_skip_day:
            self.player.stop_action()
            self.gui.set_prompt_text(
                get_text(self.lang, "actions", "save", "x")
            )
            return

        self.gui.set_prompt_text(
            get_text(self.lang, "actions", "save", "q")
        )

        if self.gui.prompt_input_buffer == pg.K_y:
            savepoint = self.player.target
            save_type = "tent" if savepoint.in_family("tent") else "cabin" if savepoint.in_family("cabin") else "outside"
            self._save(save_type)
        
        elif self.gui.prompt_input_buffer == pg.K_n:
            self.player.stop_action()

            self.gui.set_prompt_text(
                get_text(self.lang, "actions", "save", "n")
            )
        
        self.gui.prompt_input_buffer = None
    
    def _save(self, save_type):
        def _player_hurt_on_sleep():
            if not self.world.season in [SEASON_AUTUMN, SEASON_WINTER]:
                return

            get_hurt = 0.5 >= random()
            
            if get_hurt:
                health = self.player.health - randint(5, 15)
                self.player.set_health(health)

        if self.inventory.expanded:
            self.inventory.toggle_expand()

        if save_type == "outside":
            _player_hurt_on_sleep()
        
        elif save_type == "tent":
            tent = self.player.target
            is_burning_campfire = lambda child: child.in_family("campfire") and child.in_family("fire")
            burning_campfires = list( filter( is_burning_campfire, self.world.children ) )

            if burning_campfires:
                dist_to_tent = lambda child: ( pg.Vector2(tent.position) - child.position ).length()
                nearest_burning_campfire = min(burning_campfires, key=dist_to_tent)
                dist_to_nearest_burning_campfire = ( pg.Vector2(tent.position) - nearest_burning_campfire.position ).length()

                if dist_to_nearest_burning_campfire <= 150:
                    print("sleeping near campfire")
                    self.player.set_temperature(self.player.NORMAL_TEMPERATURE)
                else:
                    _player_hurt_on_sleep()
            else:
                _player_hurt_on_sleep()
            
        elif save_type == "cabin":
            print("sleeping in cabin")
            self.player.set_temperature(self.player.NORMAL_TEMPERATURE)

        self.player.stop_action()
        
        # Skip to the next day
        # self.world.next_day()
        # Moved to menu, bcs when loading new day changes
        # in world could be seen for a split second
        self.screen.fill(BLACK)

        self.gui.set_prompt_text(
            get_text(self.lang, "actions", "save", "y")
        )

        self.menu.set_run(NEW_DAY_LOADING)
        
    def delete_world(self):
        self.saveloadstream.delete_file(self.world_name)
        self.remove_world(self.world_name)
        
        if self.world_index > 0 and self.world_index != len(self.worlds)-1:
            self.set_world_index(self.world_index-1)
        
    # Program is increasing on RAM when reloading game from menu.
    def clean(self):
        self.world.clean()
        del self.world
        del self.player
        del self.inventory

    def quit(self):
        print("Quitting.")
        self.running = False


if __name__ == "__main__":
    MainGame().run()
