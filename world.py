from random import randrange, choices

from utils.classes import CannotSpawnHere
from world_spawns import GENERATION
from entities import *
from player import *


class World:

    def __init__(self, game):
        self.game = game

        self.box = Rect(0, 0, 8000, 6000)
        self.box.center = (0, 0)

        self.children = []
        self.day = 1
        self.season = SPRING

    @property
    def player(self):
        return self.game.player

    @property
    def camera(self):
        return self.game.camera

    @property
    def texture_container(self):
        return self.game.texture_container
    
    @property
    def entities(self):
        is_entity = lambda child : type(child) == Entity
        return tuple( filter(is_entity, self.children) )
    
    @property
    def items(self):
        is_item = lambda child : child.is_item
        return tuple( filter(is_item, self.children) )

    def add_child(self, child : Entity):
        if child in self.children:
            return
            
        self.children.append(child)

    def remove_child(self, child : Entity):
        if child not in self.children:
            return 

        self.children.remove(child)
    
    def generate(self):
        for gen_entry in GENERATION:
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
                        
                    n = randrange( scattered_positions[0], scattered_positions[1]+1 ) if type(scattered_positions) != int else scattered_positions
                    
                    for _ in range( randrange(n) if type(n) != int else n ):
                        data = item(spawn_id) if entity_subtype(spawn_id) == "item" else entity(spawn_id)

                        try:
                            self.spawn( (x, y), data, scatter=(scatter_x*SCALE, scatter_y*SCALE) )
                        except CannotSpawnHere:
                            continue
        
        # data = entity(ANIMAL_HARE)
        # self.spawn( (0, 0), data )

    def spawn( self, position, data, scatter=(0, 0) ):
        sx, sy = scatter
        id_ = data["id"]

        texture = self.texture_container.get(id_)
        
        spawn_position = list(position)
        spawn_position[0] += randrange(-sx, sx) if sx else 0
        spawn_position[1] += randrange(-sy, sy) if sy else 0

        new_child = Entity(data, texture, spawn_position, self)

        for child in self.children:
            if child.box.colliderect(new_child.box):
                raise CannotSpawnHere("at least 2 entity boxes are overlapping")

        self.add_child(new_child)

    def draw(self, screen):
        screen.fill(self.season)

    def run(self):
        for child in self.children:
            child.update()
            child.move(self.children)
        
    def clean(self):
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
        