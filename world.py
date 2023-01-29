from random import randrange, choices

from utils.classes import CannotSpawnHere
from world_spawns import *
from entities import *
from player import *


DAYS_IN_SEASON = 10


class World:

    def __init__(self, game):
        self.game = game

        self.box = Rect(0, 0, 8000, 6000)
        self.box.center = (0, 0)

        self.children = []
        self.day = 0

    @property
    def animals(self):
        is_animal = lambda child : child.is_animal
        return tuple( filter(is_animal, self.children) )

    @property
    def camera(self):
        return self.game.camera
    
    @property
    def color(self):
        return SEASONS_COLORS[self.season]
    
    @property
    def items(self):
        is_item = lambda child : child.is_item
        return tuple( filter(is_item, self.children) )
    
    @property
    def player(self):
        return self.game.player
    
    @property
    def season(self):
        return (self.day // DAYS_IN_SEASON) % 4

    @property
    def texture_container(self):
        return self.game.texture_container

    def add_child(self, child : Entity):
        if child in self.children:
            return
            
        self.children.append(child)

    def remove_child(self, child : Entity):
        if child not in self.children:
            return 

        self.children.remove(child)
    
    def generate(self, generation_data):
        for gen_entry in generation_data:
            grid = gen_entry["grid"]
            spawns = gen_entry["spawns"]

            spawn_grid = make_grid(self.box, grid)
            weights = tuple( map( lambda entry: entry["weight"], spawns ) )

            for y in spawn_grid[1]:
                for x in spawn_grid[0]:
                    spawn = choices(spawns, weights)[0]
                    spawn_id = spawn.get("id")
                    scatter_x, scatter_y = spawn.get( "scatter", (25, 15) )
                    scattered_positions = spawn.get( "scattered_positions", 1 )

                    if not spawn_id:
                        continue
                        
                    n = randint( scattered_positions[0], scattered_positions[1] ) if type(scattered_positions) != int else scattered_positions
                    
                    for _ in range( randrange(n) if type(n) != int else n ):
                        data = item(spawn_id) if entity_subtype(spawn_id) == "item" else entity(spawn_id)

                        try:
                            self.spawn( (x, y), data, scatter=(scatter_x*SCALE, scatter_y*SCALE) )
                        except CannotSpawnHere:
                            continue
    
    def next_day(self):
        self.day += 1

        self.random_despawns()
        self.generate(RANDOM_SPAWNS)
        self.refresh_lootable_entites()

        self.player_sleeps()
    
    def random_despawns(self):
        for child in self.children:
            for family in RANDOM_DESPAWNS:
                if not child.in_family(family):
                    continue
                
                success_chance = RANDOM_DESPAWNS[family]
                success = 100*success_chance >= randint(0, 100)

                if not success:
                    continue
                
                self.remove_child(child)
    
    def refresh_lootable_entites(self):
        for child in self.children:
            if child.in_family("interact_loot") and not child.in_family("loot"):
                success = 100*0.5 >= randint(0, 100)

                if not success:
                    continue

                child.add_family("loot")
    
    def player_sleeps(self):
        self.player.set_stamina(100)
        saturation = self.player.saturation - 20
        self.player.set_saturation(saturation)

    def spawn( self, position, data, scatter=(0, 0) ):
        sx, sy = scatter
        id_ = data["id"]
        subtype = entity_subtype(id_)

        texture = self.texture_container.get_animal_set(id_)[SOUTH][0] if subtype == "animal" else self.texture_container.get(id_)
        
        spawn_position = list(position)
        spawn_position[0] += randrange(-sx, sx) if sx else 0
        spawn_position[1] += randrange(-sy, sy) if sy else 0

        new_child = Entity(data=data, image=texture, position=spawn_position, parent=self)

        for child in self.children:
            if child.box.colliderect(new_child.box):
                raise CannotSpawnHere("at least 2 entity boxes are overlapping")

        self.add_child(new_child)

    def draw(self, screen):
        screen.fill(self.color)

    def run(self):
        for child in self.children:
            child.update()
            child.move(self.children)
        
    def clean(self):
        for child in self.children:
            del child

        self.children.clear()
    
    def load(self, data):
        self.day = data["day"]

        for child in data["children"]:
            position, child_data = child["position"], child["data"]
            self.spawn(position, child_data)
    
    @property
    def data(self):
        data = {
            "day": self.day,
            "children": []
        }

        for child in self.children:
            if child is self.player:
                continue
            
            data["children"].append(
                {
                    "position": child.position,
                    "data": child.data
                }
            )

        return data
        