from os.path import join as pathjoin, curdir
from os import remove
from json import dump, load
from player import Player
from world import World
from inventory import Inventory


FILEPATH = "savefiles"
DEFAULT_SAVEFILE = "unnamed_savefile"
FILE_EXTENSION = ".json"

DATA_PLAYER = "Player"
DATA_INVENTORY = "Inventory"
DATA_WORLD = "World"


class SaveLoadStream:

    def __init__(self, game):
        self.game = game
    
    @property
    def texture_container(self):
        return self.game.texture_container

    def save(self, filename=DEFAULT_SAVEFILE):
        file = pathjoin(FILEPATH, filename + FILE_EXTENSION)

        # ALSO, IMPLEMENT CONFIRMATION TO OVERRIDE EXITSTING SAVE FILES.

        print(f"Saving data to file \"{file}\"...")
        
        save_data = {}
        game = self.game
        save_data[DATA_PLAYER] = game.player.data
        save_data[DATA_INVENTORY] = game.inventory.data
        save_data[DATA_WORLD] = game.world.data

        with open(file, "w") as savefile:
            dump(save_data, savefile, indent=2)
        
        print("Data saved successfully.")

    def load(self, filename=DEFAULT_SAVEFILE):
        file = pathjoin(FILEPATH, filename + FILE_EXTENSION)
        
        print(f"Loading data from file \"{file}\"...")
        
        try:
            with open(file, "r") as savefile:
                load_data = load(savefile)

                self.load_world( load_data[DATA_WORLD] )
                self.load_inventory( load_data[DATA_INVENTORY] )
                self.load_player( load_data[DATA_PLAYER] )

        except FileNotFoundError:
            print(f"File \"{file}\" not found.")
            return 1
        
        print("Data loaded successfully.")

        return 0
    
    def load_world(self, world_data : dict):
        game = self.game
        
        game.world = World(game)
        game.world.load(world_data)
        game.world.next_season()
        print("Loaded World.")
    
    def load_inventory(self, inventory_data : dict):
        game = self.game
        inventory_slots = inventory_data["slots"]
        inventory_slot_index = inventory_data["slot_index"]
        cs1 = inventory_data["clothes_slot_1"]
        cs2 = inventory_data["clothes_slot_2"]

        game.inventory = Inventory(inventory_slots, game, cs1, cs2)
        game.inventory.slot_index = inventory_slot_index
        print("Loaded Inventory.")
    
    def load_player(self, player_data : dict):
        game = self.game
        parent = self.game.world
        name = player_data["name"]
        player_texture_set = self.texture_container[name]
        player_position = player_data["position"]

        game.player = Player(
            game=game,
            name=name,
            data=player_data,
            texture_set=player_texture_set,
            image=player_texture_set[0][0],
            position=player_position,
            parent=parent
        )

        game.world.add_child(game.player)
        print("Loaded Player.")
    
    def delete_file(self, filename):
        file = pathjoin(curdir, "savefiles", filename + FILE_EXTENSION)
        remove(file)
    
    def load_settings(self):
        file = "settings.json"

        print("Loading settings...")

        try:
            with open(file, "r") as settingsfile:
                settings_data = load(settingsfile)
                self.game.set_settings(settings_data)

        except FileNotFoundError:
            print(f"File \"{file}\" not found.")
            return 1
        
        print("Settings loaded successfully.")

        return 0
    
    def write_settings(self):
        file = "settings.json"

        print("Saving settings...")

        with open(file, "w") as settingsfile:
            dump(self.game.settings, settingsfile, indent=2)
    
        print("Settings saved successfully.")