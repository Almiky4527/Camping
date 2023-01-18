import pygame as pg
from pygame import mouse, key
from random import randint

from utils.classes import *
from utils.texts import *
from inventory import *
from entities import *


SPRINT_SPEED = 3
WALK_SPEED = 2

FOLIAGE_CUTTING_STAMINA_PRICE = 10
LOOTING_STAMINA_PRICE = 5
MIN_STAMINA_FOR_ACTION = 10


class Player (Entity):

    def __init__(self, game, texture_set, data : dict, *args, **kwargs):
        self.game = game

        self.texture_set = texture_set
        self.frame_time = (FPS // 4) - 1
        self.setup_texture_set()

        super().__init__(data, texture_set[SOUTH][0], *args, **kwargs)
    
    def setup_texture_set(self):
        for texture_list in self.texture_set.values():
            frame0 = texture_list[0]
            texture_list.insert(2, frame0)

    @property
    def world(self):
        return self.parent

    @property
    def camera(self):
        return self.game.camera

    @property
    def inventory(self):
        return self.game.inventory
    
    @property
    def attack_damage(self):
        item_attack_damage = self.selected_slot.get("attack_damage")
        return item_attack_damage if item_attack_damage else super().attack_damage

    @property
    def selected_slot(self):
        return self.inventory.selected_slot
    
    @property
    def can_cut_foliage(self):
        return self.selected_slot.in_family("axe") and self.stamina > FOLIAGE_CUTTING_STAMINA_PRICE
    
    @property
    def can_loot(self):
        return self.stamina > LOOTING_STAMINA_PRICE
    
    @property
    def can_light_fire(self):
        return "fire_starter" in self.selected_slot.get("family", [])
    
    @property
    def can_feed_fire(self):
        return "fire_fuel" in self.selected_slot.get("family", [])
    
    @property
    def is_attacking(self):
        if not type(self.target) == Entity:
            return False
        
        return self.target and self.target.is_alive and self.in_reach_of_action and self.action == self.attack
    
    @property
    def is_looting(self):
        if not type(self.target) == Entity:
            return False
        
        return self.target and self.in_reach_of_action and self.action == self.loot

    @property
    def is_sprinting(self):
        return self.is_moving and self.speed == SPRINT_SPEED
    
    def checkout(self):
        print(self.data)
    
    def checkout_item(self):
        print(self.selected_slot.data)

    def get_input(self, events):
        keys = key.get_pressed()
        
        self.update_vector(keys)
        self.update_speed(keys)

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_q and keys[pg.K_LSHIFT]:
                    self.drop_item(dropall=True)
                elif ev.key == pg.K_q:
                    self.drop_item()
                elif ev.key == pg.K_SPACE:
                    self.use_item()
                
                # For testing purposes.
                elif ev.key == pg.K_y:
                    self.checkout()
                elif ev.key == pg.K_h:
                    self.checkout_item()
                elif ev.key == pg.K_g:
                    self.die()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == pg.BUTTON_LEFT:
                    self.query_action()

    def move(self, *args, **kwargs):
        super().move(*args, **kwargs)

        if self.vector:
            self.frame_time += self.speed - 1
            self.frame_time %= FPS
        else:
            self.frame_time = (FPS // 4) - 1

    def update_stamina(self):
        if self.is_sprinting:
            stamina = self.stamina - (10 / FPS)
        elif self.is_moving:
            stamina = self.stamina + (5 / FPS)
        else:
            stamina = self.stamina + (10 / FPS)
        
        self.set_stamina(stamina)
        
        # Stop action when too tired
        if self.stamina < MIN_STAMINA_FOR_ACTION and self.action in (self.attack, self.loot):
            self.game.gui.set_prompt_text("You are too tired to continue.")
            self.stop_action()
            return
        
        # Replenish stamina over time when inactive
        if self.is_moving or self.is_attacking or self.is_looting or self.stamina >= 100:
            return

    def update_vector(self, keys):
        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            self.stop_action()

        if keys[pg.K_a] and keys[pg.K_d]:
            self.vector.x = 0
        elif keys[pg.K_a]:
            self.vector.x = -1
        elif keys[pg.K_d]:
            self.vector.x = 1
        else:
            self.vector.x = 0

        if keys[pg.K_w] and keys[pg.K_s]:
            self.vector.y = 0
        elif keys[pg.K_w]:
            self.vector.y = -1
        elif keys[pg.K_s]:
            self.vector.y = 1
        else:
            self.vector.y = 0
    
    def update_speed(self, keys):
        if keys[pg.K_LSHIFT] and self.stamina > 0:
            self.set_speed(SPRINT_SPEED)
        else:
            self.set_speed(WALK_SPEED)
        
    def update_image(self):
        texture_list = self.texture_set[self.direction]
        frame = self.frame_time // (FPS // 4)
        self.image = texture_list[frame]

    def query_action(self):
        target_position = position_from_screen( mouse.get_pos(), self.camera.topleft )

        for child in self.camera.scene:
            if not child.rect.collidepoint(target_position) or child is self:
                continue

            if child.is_item:
                self.action = self.pickup_item
            
            elif child.in_family("loot"):
                if not self.can_loot:
                    continue

                self.action = self.loot
            
            elif child.in_family("foliage"):
                if not self.can_cut_foliage:
                    continue
                
                self.action = self.attack
            
            elif child.in_family("plant"):
                self.action = self.attack
            
            elif child.in_family("savepoint"):
                self.action = self.game.save
            
            elif child.is_burning:
                if not self.can_feed_fire:
                    self.action = self.isnpect_fire
                else:
                    self.action = self.feed_fire
            
            elif child.in_family("campfire"):
                if not self.can_light_fire:
                    continue

                self.action = self.light_fire

            else:
                continue

            self.target = child
            self.target_position = child.position
            break
        else:
            self.stop_action()
            self.target_position = target_position
                    
    def pickup_item(self):
        item = self.target

        try:
            self.inventory.add_item(item)
            self.parent.remove_child(item)
        except ContainerFull:
            self.game.gui.set_prompt_text("Your inventory is full.")

        self.stop_action()
    
    def drop_item(self, dropall=False, slot=None):
        item_data = self.inventory.pop_item(dropall, slot)

        if not item_data:
            return

        if item_data["id"] != None:
            self.parent.spawn(self.position, item_data)
    
    def light_fire(self):
        if not self.can_light_fire:
            return

        campfire = self.target
        target_id = campfire.id
        target_name = get_name(target_id)

        if campfire.in_family("fire"):
            self.game.gui.set_prompt_text(f"The {target_name} is already lit.")
            self.stop_action()
            return

        item_id = self.selected_slot["id"]
        item_name = get_name(item_id)

        success_chance = self.selected_slot.get("success_chance")
        success = 100*success_chance >= randint(0, 100)
        self.inventory.pop(self.selected_slot)

        if success:
            campfire.light_on_fire()
            self.game.gui.set_prompt_text(f"You lit the {target_name} using your {item_name}.")
        else:
            self.game.gui.set_prompt_text(f"You struck your {item_name} but nothing happened.")

        self.stop_action()

    def feed_fire(self):
        if not self.can_feed_fire:
            return
        
        fire = self.target
        selected_item = self.selected_slot
        saturation = fire.saturation + selected_item["fire_fuel"]

        if saturation > 100:
            self.game.gui.set_prompt_text("There is no need to feed the fire right now.")
            self.stop_action()
            return
        
        fire.set_saturation(saturation)
        self.inventory.pop(self.selected_slot)

        self.game.gui.set_prompt_text("You put a log on the fire.")
        self.stop_action()
    
    def isnpect_fire(self):
        fire = self.target
        saturation = fire.saturation

        if not saturation:
            return
        elif saturation >= 80:
            self.game.gui.set_prompt_text("The fire is in a great condition.")
        elif saturation >= 20:
            self.game.gui.set_prompt_text("The fire could use a couple of logs.")
        else:
            self.game.gui.set_prompt_text("The fire is almost burnt out.")
        
        self.stop_action()
    
    def attack(self):
        if self.action_time >= self.attack_cooldown * FPS:
            self.target.damage(self.attack_damage)
            
            stamina = self.stamina - FOLIAGE_CUTTING_STAMINA_PRICE
            self.set_stamina(stamina)
            
            self.action_time = 0
        else:
            self.action_time += 1
        
        if not self.target.is_alive:
            self.stop_action()
    
    def loot(self):
        target_name = get_name(self.target.id)
        self.game.gui.set_prompt_text(f"You search the {target_name} for some berries...")

        stamina = self.stamina - (LOOTING_STAMINA_PRICE / FPS)
        self.set_stamina(stamina)

        if self.action_time >= self.target.looting_time * FPS:
            target = self.target
            loot = target.data.get("interact_loot")
            target.spawn_loot(loot)
            target.rm_family("loot")

            self.action_time = 0
        else:
            self.action_time += 1

        if not self.target.in_family("loot"):
            self.stop_action()

    def use_item(self):
        if not self.selected_slot:
            return

        if self.selected_slot.in_family("spawn"):
            self.spawn_entity()
        elif self.selected_slot.in_family("food"):
            self.eat_item()
        else:
            pass
    
    def spawn_entity(self):
        spawn_id = self.selected_slot.get("spawn")
        spawn_subtype = entity_subtype(spawn_id)
        spawn_data = item(spawn_id) if spawn_subtype == "item" else entity(spawn_id)
        position = self.position[0], self.box.top - SCALE

        try:
            self.world.spawn(position, spawn_data)
            self.inventory.pop(self.selected_slot)

            entity_name = get_name(spawn_id)
            self.game.gui.set_prompt_text(f"Placed a {entity_name}.")
        except CannotSpawnHere:
            self.game.gui.set_prompt_text("You cannot place that here right now.")
    
    def eat_item(self):
        food_value = self.selected_slot.get("food")
        item_id = self.selected_slot["id"]

        if self.saturation + food_value > 100:
            self.game.gui.set_prompt_text("You are not hungry enough to eat this.")
        else:
            self.set_saturation(self.saturation + food_value)
            self.inventory.pop(self.selected_slot)
            item_name = get_name(item_id)
            self.game.gui.set_prompt_text(f"You ate some delicous {item_name}.")

    def update(self):
        super().update()

        self.update_image()
        self.update_stamina()
    
    def die(self):
        self.set_health(0)
        self.parent.remove_child(self)

        self.spawn_loot()
        self.inventory.clear()
    
    def spawn_loot(self):
        for item_data in self.inventory:
            if not item_data:
                continue

            self.world.spawn( self.position, item_data, scatter=(40, 30) )