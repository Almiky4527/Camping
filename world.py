from random import randrange, choices, randint, random

from utils.classes import CannotSpawnHere
from utils.identifiers import *
from world_spawns import *
from entities import *
from player import *


class World:
    DAYS_IN_SEASON = 10
    TIME_TO_SKIP = 60
    MAX_ANIMAL_CAP = 5

    def __init__(self, game):
        self.game = game

        self.box = Rect(0, 0, 8000, 6000)
        self.box.center = (0, 0)

        self.children = []
        self.day = 0
        self.day_uptime = 0

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
    def season(self) -> int:
        return (self.day // self.DAYS_IN_SEASON) % 4
    
    @property
    def seconds(self) -> int:
        return self.day_uptime // FPS
    
    @property
    def can_skip_day(self) -> bool:
        return self.seconds >= self.TIME_TO_SKIP
    
    @property
    def animal_cap_reached(self) -> bool:
        return len(self.animals) == self.MAX_ANIMAL_CAP

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
    
    def list_chidren_in_family(self, family : str):
        _filter = lambda child: child.in_family(family)
        return list( filter(_filter, self.children) )
    
    def generate(self, generation_data):
        for gen_entry in generation_data:
            grid = gen_entry["grid"]
            spawns = gen_entry["spawns"]

            if not spawns:
                continue

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
        self.day_uptime = 0

        if self.day % self.DAYS_IN_SEASON == 0:
            self.next_season()

        spawns = RANDOM_SPAWNS[self.season]
        animals = RANDOM_ANIMAL_SPAWNS[self.season]

        self.random_despawns()
        self.despawn_animals()
        self.generate(spawns)
        self.spawn_animals(animals)
        self.refresh_lootable_entites()
        self.apply_random_hunger_to_entities()
        self.player_sleeps()
    
    def next_season(self):
        if self.season == SEASON_SPRING:
            self.configure_for_season_spring()
        elif self.season == SEASON_SUMMER:
            self.configure_for_season_summer()
        elif self.season == SEASON_AUTUMN:
            self.configure_for_season_autumn()
        elif self.season == SEASON_WINTER:
            self.configure_for_season_winter()

    def configure_for_season_spring(self):
        for child in self.children:
            if not child.is_immobile:
                continue
            
            if entity_subtype(child.id) in ["tree", "bush", "building"]:
                default_texture = self.texture_container.get(child.id)
                try:
                    season_appropriate_texture = self.texture_container.get("spring." + child.id)
                except KeyError:
                    season_appropriate_texture = default_texture
                child.set_image(season_appropriate_texture)

    def configure_for_season_summer(self):
        for child in self.children:
            if not child.is_immobile:
                continue
            
            if entity_subtype(child.id) in ["tree", "bush", "building"]:
                default_texture = self.texture_container.get(child.id)
                try:
                    season_appropriate_texture = self.texture_container.get("summer." + child.id)
                except KeyError:
                    season_appropriate_texture = default_texture
                child.set_image(season_appropriate_texture)

    def configure_for_season_autumn(self):
        for child in self.children:
            if not child.is_immobile:
                continue
            
            if entity_subtype(child.id) in ["tree", "bush", "building"]:
                default_texture = self.texture_container.get(child.id)
                try:
                    season_appropriate_texture = self.texture_container.get("autumn." + child.id)
                except KeyError:
                    season_appropriate_texture = default_texture
                child.set_image(season_appropriate_texture)

    def configure_for_season_winter(self):
        bushes = self.list_chidren_in_family("bush")

        for bush in bushes:
            if bush.in_family("interact_loot") and bush.in_family("loot"):
                bush.rm_family("loot")

        for child in self.children:
            if not child.is_immobile:
                continue
            
            if entity_subtype(child.id) in ["tree", "bush", "building"]:
                default_texture = self.texture_container.get(child.id)
                try:
                    season_appropriate_texture = self.texture_container.get("winter." + child.id)
                except KeyError:
                    season_appropriate_texture = default_texture
                child.set_image(season_appropriate_texture)
        
        plants = self.list_chidren_in_family("plant")

        for plant in plants:
            self.remove_child(plant)
    
    def random_despawns(self):
        for family, despawn_chance in RANDOM_DESPAWNS.items():
            children_in_this_family = self.list_chidren_in_family(family)

            for child in children_in_this_family:
                do_despawn = despawn_chance >= random()

                if not do_despawn:
                    continue

                self.remove_child(child)
    
    def refresh_lootable_entites(self):
        if self.season in [SEASON_AUTUMN, SEASON_WINTER]:
            return

        for child in self.children:
            if not child.in_family("interact_loot") or child.in_family("loot"):
                continue
            
            success = 0.5 >= random()

            if not success:
                continue

            child.add_family("loot")
    
    def apply_random_hunger_to_entities(self):
        for child in self.children:
            if not child.saturation:
                continue

            saturation = child.saturation - randint(20, 30)
            child.set_saturation(saturation)
    
    def despawn_animals(self):
        for animal in self.animals:
            self.remove_child(animal)

    def spawn_animals(self, spawn_data):
        for entry in spawn_data:
            animal_id = entry["id"]
            count = entry["count"]
            chance = entry.get("chance", 1)
            distance_to_player = entry["dtp"]

            success = 100*chance >= randint(0, 100)

            if not success:
                continue
                
            animal_data = entity(animal_id)
            count = randint( *count ) if type(count) != int else count
            x, y = self.box.x, self.box.y
            w, h = self.box.w, self.box.h

            for _ in range(count):
                if self.animal_cap_reached:
                    return

                while True:
                    position = randint(x + 10, x + w - 10), randint(y + 10, y + h - 10)
                    vector_to_player = Vector2(
                        self.player.position[0] - position[0],
                        self.player.position[1] - position[1]
                    )
                    
                    if vector_to_player.length() > distance_to_player:
                        break
                
                self.spawn(position, animal_data)
    
    def player_sleeps(self):
        self.player.set_stamina(100)

        energy_plus = max(50, self.player.saturation)
        self.player.set_energy(self.player.energy + energy_plus)
        self.player.energy_warned = False

        if self.player.saturation == 0:
            health = self.player.health - randint(20, 30)
            self.player.set_health(health)
        elif self.player.saturation >= 20:
            health = self.player.health + randint(10, 30)
            self.player.set_health(health)

    def spawn( self, position, data, scatter=(0, 0) ):
        sx, sy = scatter
        id_ = data["id"]
        subtype = entity_subtype(id_)

        texture_set = self.texture_container.get_animal_set(id_) if subtype == "animal" else None
        texture = texture_set[SOUTH][0] if texture_set else self.texture_container.get(id_)
        
        spawn_position = list(position)
        spawn_position[0] += randrange(-sx, sx) if sx else 0
        spawn_position[1] += randrange(-sy, sy) if sy else 0

        new_child = Entity(data=data, image=texture, texture_set=texture_set, position=spawn_position, parent=self)

        for child in self.children:
            if child.box.colliderect(new_child.box):
                raise CannotSpawnHere("at least 2 entity boxes are overlapping")

        self.add_child(new_child)

    def draw(self, screen):
        screen.fill(self.color)

    def run(self):
        self.day_uptime += 1

        for child in self.children:
            child.update()
            child.move(self.children)
        
        # Skip to next day when player runs out of energy
        if self.player.energy == 0:
            self.game._save("outside")
        
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
        