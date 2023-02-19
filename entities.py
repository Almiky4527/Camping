import pygame as pg
from pygame.math import Vector2
from random import randrange, randint

from utils.identifiers import *
from utils.classes import *
from utils.functions import *
from utils.display import SCALE, FPS

from entity_data import *


class Entity (BaseEntity):

    NO_FAMILY = ()

    def __init__(self, data : dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data
        self.id = data["id"]

        # *** FIX THIS ****************************************
        self.family = data.get("family", self.NO_FAMILY).copy()
        self.data["family"] = self.family
        # *****************************************************

        self.reach = pg.Rect(0, 0, 0, 0)
        box_size = data.get("box_size")
        reach_size = data.get("reach_size")

        if box_size:
            self.set_box_size(box_size)
        
        if reach_size:
            self.reach.size = Vector2(reach_size) * SCALE

        self.vector = Vector2()

        self.target = None
        self.target_position = None
        self.action = None
        self.action_time = 0
    
    @property
    def attack_cooldown(self):
        return self.data.get("attack_cooldown")

    @property
    def attack_damage(self):
        return self.data.get("attack_damage", 0)

    @property
    def count(self):
        return self.data.get("count")
    
    @property
    def default_speed(self):
        return self.data.get("default_speed", 0)
    
    @property
    def direction(self):
        return self.data.get("direction", SOUTH)
    
    @property
    def direction_to_action(self):
        return directionalize(self.vector_to_action)

    @property
    def max_health(self):
        return self.data.get("max_health")
    
    @property
    def max_speed(self):
        return self.data.get("max_speed")
    
    @property
    def health(self):
        return self.data.get("health")
    
    @property
    def is_alive(self):
        return bool(self.health)
    
    @property
    def is_animal(self):
        return self.in_family("animal")
    
    @property
    def is_burning(self):
        return self.in_family("fire")
    
    @property
    def is_dead(self):
        return not self.is_alive and not self.is_immortal
    
    @property
    def is_immobile(self):
        return self.data.get("immobile", False) or self.is_item
    
    @property
    def is_immortal(self):
        return self.health is None
    
    @property
    def is_item(self):
        return self.in_family("item")
    
    @property
    def is_interactable(self):
        return self.in_family("interact")
    
    @property
    def is_moving(self):
        return bool(self.vector)
    
    @property
    def is_player(self):
        return self.id == ENTITY_PLAYER
    
    @property
    def in_reach_of_action(self):
        if self.target:
            if self.target.box:
                return self.reach.colliderect(self.target.box)
        return self.in_reach(self.target_position)
    
    @property
    def loot(self):
        return self.data.get("loot")
    
    @property
    def looting_time(self):
        return self.data.get("looting_time", 0)
    
    @property
    def num_of_frames(self):
        return len(self.texture_list) if self.texture_list else 1
    
    @property
    def possible_targets(self):
        return self.data.get("possible_targets", [])
    
    @property
    def run_away_from(self):
        return self.data.get("run_away_from", [])
    
    @property
    def spawn(self):
        return self.data.get("spawn")

    @property
    def speed(self):
        return self.data.get("speed", 0)
    
    @property
    def stamina(self):
        return self.data.get("stamina")

    @property
    def saturation(self):
        return self.data.get("saturation")
    
    @property
    def texture_list(self):
        return self.texture_set[self.direction] if self.texture_set else []
    
    @property
    def vector_to_action(self):
        if not self.target_position:
            return Vector2()

        v = Vector2(self.target_position) - self.position
        v.x = 0 if abs(v.x) < SCALE else v.x
        v.y = 0 if abs(v.y) < SCALE else v.y
        return v
    
    def in_family(self, value : str):
        if not self.family:
            return False
        
        return value in self.family
    
    def add_family(self, value : str):
        self.data["family"].append(value)
    
    def rm_family(self, value : str):
        self.data["family"].remove(value)

    def in_reach(self, position):
        return self.reach.collidepoint(position) if position else False
    
    def set_health(self, value : int):
        self.data["health"] = max( 0, min(value, self.max_health) )
    
    def set_speed(self, value : int):
        self.data["speed"] = max( 0, min(value, self.max_speed) )
    
    def set_position(self, position):
        super().set_position(position)

        self.reach.center = position
        self.data["position"] = tuple(self.position)

    def set_direction(self, value : int):
        self.data["direction"] = max( 0, min(value, 3) )
    
    def set_stamina(self, value : int):
        self.data["stamina"] = round( max( 0, min(value, 100) ), 2 )

    def set_saturation(self, value : int):
        self.data["saturation"] = max( 0, min(value, 100) )
    
    def set_box_size(self, size):
        position = self.position
        scaled_size = size[0] * SCALE, size[1] * SCALE
        self.box.size = scaled_size
        self.set_position(position)
    
    def damage(self, value : int):
        if not self.health:
            return

        health = self.health - value
        self.set_health(health)
    
    def burn(self):
        if not self.is_burning:
            return

        saturation = self.saturation - ( 0.065 / FPS )  # x amount of saturation will be taken after 1 second
        self.set_saturation(saturation)                 # 0.065 saturation pre second, 3.9/min, cca 25.5 min burning time

        self.frame_time += 1
        self.frame_time %= FPS

        if self.saturation == 0:
            self.stop_burning()
        
    def light_on_fire(self):
        self.add_family("fire")
        self.set_saturation(100)
        self.set_texture_set(self.parent.texture_container[self.id + BURNING_SUBTYPE])
    
    def stop_burning(self):
        self.rm_family("fire")
        self.texture_set = None
        self.image = self.parent.texture_container.get(self.id)
        self.frame_time = 0
    
    def clip_x(self, entity):
        x = self.vector.x

        if x > 0:
            self.set_box_right(entity.box.left)
        if x < 0:
            self.set_box_left(entity.box.right)
    
    def move_x(self, entities):
        self.set_x(self.x + self.vector.x * self.speed)

        for entity in entities:
            if entity is self:
                continue

            if self.collision(entity):
                self.clip_x(entity)
        
        # Only player cannot leave "world's borders".
        if not self.id == ENTITY_PLAYER:
            return

        if self.box.left < self.parent.box.left:
            self.set_box_left(self.parent.box.left)
        if self.box.right > self.parent.box.right:
            self.set_box_right(self.parent.box.right)
    
    def clip_y(self, entity):
        y = self.vector.y

        if y > 0:
            self.set_box_bottom(entity.box.top)
        if y < 0:
            self.set_box_top(entity.box.bottom)

    def move_y(self, entities):
        self.set_y(self.y + self.vector.y * self.speed)

        for entity in entities:
            if entity is self:
                continue

            if self.collision(entity):
                self.clip_y(entity)
            
            # Run away or attack entity
            if self.is_scared_of_entity(entity):
                self.start_running()
                self.action = self.stop_running
            
            elif self.is_entity_possible_target(entity):
                self.target = entity
                self.target_position = entity.position
                self.start_running()
                self.action = self.attack
        
        # Only player cannot leave "world's borders".
        if not self.id == ENTITY_PLAYER:
            return
        
        if self.box.top < self.parent.box.top:
            self.set_box_top(self.parent.box.top)
        if self.box.bottom > self.parent.box.bottom:
            self.set_box_bottom(self.parent.box.bottom)
    
    def move(self, entities):
        if not self.vector and (self.texture_list or self.texture_set) and not self.is_burning:
            self.frame_time = (FPS // self.num_of_frames) - 1

        if self.is_immobile:
            return
        
        self.move_x(entities)
        self.move_y(entities)

        if self.vector:
            self.frame_time += self.speed - 0.5
            self.frame_time %= FPS
        else:
            pass
    
    def move_to_action(self):
        if self.target:
            self.target_position = self.target.position

        if self.target_position and not self.in_reach_of_action:
            self.vector = self.direction_to_action
        elif self.target_position:
            self.stop_moving()
        
    def set_random_target_position(self):
        max_dist = self.data.get("max_travel_dist", 100)
        x, y = randrange(-max_dist, max_dist), randrange(-max_dist, max_dist)
        self.target_position = self.position[0] + x, self.position[1] + y

    def run_action(self):
        if not self.action:
            return

        if self.is_immobile and self.action:
            self.action()
        elif self.target and self.in_reach_of_action:
            self.action()
        elif self.is_animal and self.in_reach_of_action:
            self.action()

    def attack(self):
        if self.action_time >= self.attack_cooldown * FPS:
            self.target.damage(self.attack_damage)
            
            if self.stamina:
                stamina = self.stamina - 5
                self.set_stamina(stamina)
            
            self.action_time = 0
        else:
            self.action_time += 1
        
        if not self.target.is_alive:
            self.stop_action()

            if self.is_animal:
                self.stop_running()
    
    def forget_target(self):
        self.stop_action()
        self.stop_running()
        self.stop_moving()
    
    def stop_action(self):
        self.target = None
        self.target_position = None
        self.action = None
        self.action_time = 0
    
    def stop_moving(self):
        self.vector.update(0)
    
    def start_running(self):
        self.set_speed(self.max_speed)

    def stop_running(self):
        self.set_speed(self.default_speed)
        self.target_position = tuple(self.position)
        self.action = lambda: self.wait(3)
    
    def is_entity_possible_target(self, entity):
        if entity is self or not self.possible_targets:
            return False
        
        for targetting_data in self.possible_targets:
            family = targetting_data["family"]
            see_dist = targetting_data["see_dist"]
            forget_dist = targetting_data["forget_dist"]
            
            if not entity.in_family(family):
                continue
            
            vector_to_entity = Vector2(entity.position[0] - self.position[0], entity.position[1] - self.position[1])

            if vector_to_entity.length() >= forget_dist and entity is self.target:
                self.forget_target()
                continue

            if vector_to_entity.length() > see_dist:
                continue

            return True
        
        return False
    
    def is_scared_of_entity(self, entity):
        if entity is self or not self.run_away_from:
            return False

        for run_data in self.run_away_from:
            family = run_data["family"]
            see_dist = run_data["see_dist"]
            run_dist = run_data["run_dist"]

            if not entity.in_family(family):
                continue

            vector_to_entity = Vector2(entity.position[0] - self.position[0], entity.position[1] - self.position[1])

            if vector_to_entity.length() > see_dist:
                continue
            
            run_to_pos = self.position + vector_to_entity * (-run_dist)
            self.target_position = run_to_pos
            return True
        
        return False
    
    def update_direction(self):
        x, y = self.vector
        self.set_direction( SOUTH if y == 1 else NORTH if y == -1 else EAST if x == 1 else WEST if x == -1 else self.direction )
    
    def update(self):
        super().update()

        if not self.is_immobile and not self.is_item:
            self.move_to_action()
            self.update_direction()
        
        self.run_action()

        if self.is_animal:
            self.update_random_travel()

        if self.is_burning:
            self.burn()
        
        if self.is_dead:
            self.die()
    
    def update_random_travel(self):
        if self.is_moving or self.action:
            return

        success_chance = self.data.get("travel_chance", 0)
        success = 100*success_chance >= randint(0, 100)

        if success:
            self.stop_action()
            self.action = self.wait
            self.set_random_target_position()
    
    def wait(self, sec=5):
        if self.action_time < sec*FPS:
            self.action_time += 1
        else:
            self.stop_action()
    
    def update_image(self):
        if self.in_family("loot"):
            self.image = self.parent.texture_container.get(self.id + LOOT_SUBTYPE)
        elif self.parent.season == SEASON_WINTER:
            pass
        elif self.in_family("interact_loot"):
            self.image = self.parent.texture_container.get(self.id)

        if not self.texture_list:
            return

        frame_index = round( self.frame_time // ( FPS // self.num_of_frames ) )
        self.set_image( self.texture_list[frame_index] )
        
    def draw(self, screen, *args, **kwargs):
        self.update_image()
        super().draw(screen, *args, **kwargs)

    def die(self):
        self.set_health(0)
        self.parent.remove_child(self)

        if self.loot:
            self.spawn_loot(self.loot)
    
    def spawn_loot(self, loot):
        if not loot:
            return
        
        for item_id, item_count in loot.items():
            count = randrange( item_count[0], item_count[1]+1 ) if type(item_count) == list else item_count
            
            for _ in range(count):
                item_data = item(item_id)
                self.parent.spawn( self.position, item_data, scatter=(40, 30) )
