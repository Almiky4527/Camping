from random import randrange, choice, choices

from utils.classes import CannotSpawnHere
from entities import *
from player import *


SPAWNS_STURCTURE = [
    [ (None, 2), (PINE_SMALL, 1), (PINE_LARGE, 1), (OAK_SMALL, 1), (OAK_LARGE, 1) ],
    [ (None, 40), (ROCK0, 2), (ROCK1, 2), (ROCK2, 1), (ROCK3, 2), (ROCK4, 2) ],
    [ (None, 20), (BUSH_LARGE, 1), (BUSH_SMALL, 1) ],
    [ (None, 40), (PLANT0, 3), (PLANT1, 3), (PLANT2, 1), (PLANT3, 1) ]
]


class World:

    def __init__(self, game):
        self.game = game

        self.box = Rect(0, 0, 7000, 5000)
        self.box.center = (0, 0)

        self.children = []
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
        tree_ids = [None, PINE_SMALL, PINE_LARGE, OAK_SMALL, OAK_LARGE]
        tree_weights = [2, 1, 1, 1, 1]
        rock_ids = [None, ROCK0, ROCK1, ROCK2, ROCK3, ROCK4]
        rock_weights = (40, 2, 2, 1, 2, 2)
        bush_ids = [None, BUSH_LARGE, BUSH_SMALL]
        bush_weights = (20, 1, 3)
        plant_ids = [None, PLANT0, PLANT1, PLANT2, PLANT3]
        plant_weights = (40, 3, 3, 1, 1)

        instances = 36, 20
        spawn_grid = make_grid(self.box, instances)

        # Trees
        for y in spawn_grid[1]:
            for x in spawn_grid[0]:
                tree_id = choices(tree_ids, tree_weights)[0]

                if not tree_id:
                    continue

                data = entity(tree_id)

                try:
                    self.spawn( (x, y), data, scatter=( 25*SCALE, 15*SCALE ) )
                except CannotSpawnHere:
                    continue
        
        # Rocks
        for y in spawn_grid[1]:
            for x in spawn_grid[0]:
                rock_id = choices(rock_ids, rock_weights)[0]

                if not rock_id:
                    continue
                    
                data = item(rock_id)
                self.spawn( (x, y), data, scatter=( 50*SCALE, 30*SCALE ) )
        
        # Bushes
        for y in spawn_grid[1]:
            for x in spawn_grid[0]:
                bush_id = choices(bush_ids, bush_weights)[0]

                if not bush_id:
                    continue
                    
                data = entity(bush_id)
                self.spawn( (x, y), data, scatter=( 50*SCALE, 30*SCALE ) )
        
        # Plants
        for y in spawn_grid[1]:
            for x in spawn_grid[0]:
                plant_id = choices(plant_ids, plant_weights)[0]

                if not plant_id:
                    continue
                
                for _ in range( randrange(1, 4) ):
                    data = entity(plant_id)
                    self.spawn( (x, y), data, scatter=( 50*SCALE, 30*SCALE ) )

    def load(self, data):
        for child in data["Children"]:
            position, child_data = child["position"], child["data"]
            self.spawn(position, child_data)

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
    
    @property
    def data(self):
        data = {
            "Children": []
        }

        for child in self.children:
            if child is self.player:
                continue
            
            data["Children"].append(
                {
                    "position": child.position,
                    "data": child.data
                }
            )

        return data
        