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
ATTACK_STAMINA_PRICE = 5
LOOTING_STAMINA_PRICE = 0.05
MIN_STAMINA_FOR_ACTION = 0


class Player (Entity):
    NORMAL_TEMPERATURE = 37
    NORMAL_TEMPERATURE_RANGE = [36.5, 37.5]

    def __init__(self, game, name="JohnDoe", *args, **kwargs):
        self.game = game
        self.name = name
        super().__init__(*args, **kwargs)
        self.data["name"] = name
        
        self.energy = 100
        self.energy_warned = False

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
    def lang(self):
        return self.game.gui.lang
    
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
    def can_attack(self):
        return self.selected_slot.in_family("weapon") and self.stamina > ATTACK_STAMINA_PRICE
    
    @property
    def can_shoot(self):
        return self.selected_slot.in_family("projectile_shooter")
    
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
    def temperature(self):
        return self.data["temperature"]
    
    @property
    def cold(self):
        return round( abs( 1 - min( self.temperature / self.NORMAL_TEMPERATURE_RANGE[0], 1 ) ), 2 )
    
    @property
    def hot(self):
        return round( abs( 1 - max( self.temperature / self.NORMAL_TEMPERATURE_RANGE[1], 1 ) ), 2 )
    
    @property
    def warmth(self):
        clothes_slot_1, clothes_slot_2 = self.inventory.clothes_slot_1, self.inventory.clothes_slot_2
        return clothes_slot_1.get("warmth", 0) + clothes_slot_2.get("warmth", 0)
    
    @property
    def is_warming_up(self):
        return self.action == self.warm_up

    @property
    def is_sprinting(self):
        return self.is_moving and self.speed == SPRINT_SPEED
    
    def checkout(self):
        print(self.data)
    
    def checkout_item(self):
        print(self.selected_slot.data)

    def set_energy(self, value : int):
        self.energy = max( 0, min(value, 100) )
    
    def set_temperature(self, value: int):
        self.data["temperature"] = value
    
    def set_attack_cooldown(self, value : float):
        self.data["attack_cooldown"] = max(0, value)

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
                elif ev.key == pg.K_p:
                    self.checkout()
                elif ev.key == pg.K_i:
                    self.checkout_item()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == pg.BUTTON_LEFT:
                    self.query_action()

    def move(self, *args, **kwargs):
        super().move(*args, **kwargs)

    def update_stamina(self):
        # Replenish stamina over time when inactive
        if self.is_attacking or self.is_looting:
             # Stop action when too tired
            if self.stamina == MIN_STAMINA_FOR_ACTION:
                self.game.gui.set_prompt_text(
                    get_text(self.lang, "actions", "tired")
                )
                self.stop_action()
            return

        stamina = self.stamina

        if self.is_sprinting:
            if self.hot >= 0.13:
                stamina = self.stamina - (14 / FPS)
            elif self.hot >= 0.07:
                stamina = self.stamina - (12 / FPS)
            elif self.hot >= 0.03:
                stamina = self.stamina - (11 / FPS)
            else:
                stamina = self.stamina - (10 / FPS)
        elif not self.is_moving:
            if self.cold >= 0.15:
                stamina = self.stamina + (2 / FPS)
            elif self.cold >= 0.08:
                stamina = self.stamina + (3 / FPS)
            elif self.cold >= 0.03:
                stamina = self.stamina + (4 / FPS)
            else:
                stamina = self.stamina + (5 / FPS)
        
        self.set_stamina(stamina)
    
    def update_saturation(self):
        stamina_percentage = self.stamina / 100
        saturation_dif = (1 - stamina_percentage)*0.5 / FPS
        saturation = self.saturation - saturation_dif
        self.set_saturation(saturation)

    def update_energy(self):
        stamina_percentage = self.stamina / 100
        energy_dif = (1 - stamina_percentage)*1.0 / FPS
        energy = self.energy - energy_dif
        self.set_energy(energy)

        if self.energy <= 10 and not self.energy_warned:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "energy_low")
            )
            self.energy_warned = True
        
    def update_temperature(self):
        world_temp = self.world.temperature
        
        if self.cold >= 0.10:
            health = self.health - 1 / FPS
            self.set_health(health)

        if self.cold >= 0.02:
            self.set_attack_cooldown(0.8)
        else:
            self.set_attack_cooldown(0.5)

        if world_temp + 10.4 < self.temperature < world_temp + 10.6:
            return

        if world_temp + 10.5 < self.temperature and not self.is_warming_up:
            dif = ( 0.05 - (self.warmth/20) ) / FPS
            temp = self.temperature - dif
            self.set_temperature(temp)
        elif world_temp + 10.5 > self.temperature:
            dif = ( 0.03 + (self.warmth/20) ) / FPS
            temp = self.temperature + dif
            self.set_temperature(temp)

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

    def query_action(self):
        target_position = position_from_screen( mouse.get_pos(), self.camera.topleft )

        if self.can_shoot:
            self.shoot(target_position)
            return

        for child in self.camera.scene:
            if not child.rect.collidepoint(target_position) or child is self:
                continue

            if child.is_item:
                self.action = self.pickup_item
            
            elif child.in_family("trap"):
                self.action = self.attack
            
            elif child.in_family("loot"):
                self.action = self.loot
            
            elif child.in_family("hare"):
                if not self.can_attack:
                    continue

                self.action = self.attack
            
            elif child.in_family("foliage"):
                if child.in_family("bush") and self.selected_slot.in_family("stone_blade"):
                    self.action = self.attack
                elif not self.can_cut_foliage:
                    continue
                
                self.action = self.attack
            
            elif child.in_family("plant"):
                self.action = self.attack
            
            elif child.in_family("foundation"):
                self.action = self.build
            
            elif child.in_family("savepoint"):
                self.action = self.game.save
            
            elif child.in_family("campfire"):
                if not child.is_burning:
                    if not self.can_light_fire:
                        continue

                    self.action = self.light_fire
                else:
                    if not self.can_feed_fire:
                        if self.selected_slot.in_family("cookable"):
                            self.action = self.cook
                        else:
                            self.action = self.isnpect_fire
                    else:
                        self.action = self.feed_fire

            else:
                continue

            self.target = child
            self.target_position = child.position
            break
        else:
            self.stop_action()
            self.target_position = target_position
        
    def shoot(self, target_position):
        def _scan_inventory_for_ammunition(ammo_id):
            for slot in self.inventory:
                if not slot:
                    continue

                if slot["id"] == ammo_id:
                    return self.inventory.pop(slot)["projectile"]
                
            return 
        
        projectile_shooter = self.selected_slot
        ammunition_id = projectile_shooter["ammunition"]
        projectile_entity_id = _scan_inventory_for_ammunition(ammunition_id)

        if not projectile_entity_id:
            return
        
        durability = projectile_shooter.durability - randint(10, 20)
        projectile_shooter.set_durability(durability)

        if projectile_shooter.durability == 0:
            self.inventory.pop(projectile_shooter)

        vector_to_position = Vector2(target_position) - self.position
        projectile_data = entity(projectile_entity_id)
        projectile_entity = self.world.spawn(self.position, projectile_data)
        projectile_entity.target_position = target_position
        projectile_entity.action = projectile_entity.projectile_hit
        
        angle = Vector2(-1, 1).angle_to(-vector_to_position)
        image = projectile_entity.image
        image = pg.transform.rotate(image, -angle)
        projectile_entity.set_image(image)
    
    def build(self):
        if not self.selected_slot:
            self.stop_action()
            return

        target = self.target
        required_build_materials = target.data["required_build_materials"]
        item_id = self.selected_slot["id"]

        for entry in required_build_materials:
            item_s, amount_required = entry[0], entry[1]

            if not item_id in item_s or amount_required == 0:
                continue

            self.inventory.pop(self.selected_slot)
            entry[1] -= 1
            
            stamina = self.stamina - ( 10 + self.hot*100 )
            self.set_stamina(stamina)
        
        get_amount = lambda entry: entry[1]
        building_finished = sum( map(get_amount, required_build_materials) ) == 0
        
        if building_finished:
            building = target.data["output_building"]
            building_data = entity(building)

            self.world.remove_child(self.target)
            self.world.spawn(self.target.position, building_data)
        
        self.stop_action()
    
    def cook(self):
        if not self.selected_slot:
            self.stop_action()
            return

        cooking_gives = self.selected_slot.data["cooking_gives"]
        self.inventory.pop(self.selected_slot)
        self.parent.spawn( self.position, item(cooking_gives) )

        self.stop_action()

    def pickup_item(self):
        item = self.target

        try:
            self.inventory.add_item(item)
            self.parent.remove_child(item)
        except ContainerFull:
            self.game.gui.set_prompt_text(
                get_text(self.lang,"actions","inventory_full")
            )

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

        target = self.target
        target_id = target.id
        target_name = get_name(target_id, self.lang)

        if target.in_family("fire"):
            self.game.gui.set_prompt_text(
                get_text(self.lang,"actions","fire","already_lit").format(target=target_name)
            )
            self.stop_action()
            return

        item_id = self.selected_slot["id"]
        item_name = get_name(item_id, self.lang)

        success_chance = self.selected_slot.get("success_chance")
        success = 100*success_chance >= randint(0, 100)
        self.inventory.pop(self.selected_slot)

        if success:
            target.light_on_fire()
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "lit").format(target=target_name, item=item_name)
            )
            self. action = self.warm_up
        else:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "fail").format(item=item_name)
            )
            self.stop_action()

    def feed_fire(self):
        if not self.can_feed_fire:
            return
        
        target = self.target
        selected_item = self.selected_slot
        item_id = self.selected_slot["id"]
        item_name = get_name(item_id, self.lang)
        
        saturation = target.saturation + selected_item["fire_fuel"]

        if saturation > 100:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "no_feed")
            )
            self.stop_action()
            return
        
        target.set_saturation(saturation)
        self.inventory.pop(self.selected_slot)
        self.game.gui.set_prompt_text(
            get_text(self.lang ,"actions", "fire", "feed").format(item=item_name)
        )

        # self.stop_action()
        self. action = self.warm_up
    
    def isnpect_fire(self):
        fire = self.target
        saturation = fire.saturation

        if not saturation:
            return
        elif saturation >= 80:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "inspect", 0)
            )
        elif saturation >= 20:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "inspect", 1)
            )
        else:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "fire", "inspect", 2)
            )
        
        # self.stop_action()
        self. action = self.warm_up
    
    def warm_up(self):
        dif = ( 0.01 + (self.warmth/20) ) / FPS
        temp = self.temperature + dif
        self.set_temperature(temp)
    
    def loot(self):
        target_name = get_name(self.target.id, self.lang)
        self.game.gui.set_prompt_text(
            get_text(self.lang, "actions", "loot", "search").format(target=target_name)
        )

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
            stamina = self.stamina - ( ( 10 + self.hot*10 ) / FPS )
            self.set_stamina(stamina)

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

            entity_name = get_name(spawn_id, self.lang)
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "place", "success").format(thing=entity_name)
            )
        except CannotSpawnHere:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "place", "fail")
            )
    
    def eat_item(self):
        food_value = self.selected_slot.get("food", 0)
        item_id = self.selected_slot["id"]

        if self.saturation + food_value > 100:
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "eat", "fail")
            )
        else:
            self.set_saturation(self.saturation + food_value)
            self.inventory.pop(self.selected_slot)
            item_name = get_name(item_id, self.lang)
            self.game.gui.set_prompt_text(
                get_text(self.lang, "actions", "eat", "success").format(food=item_name)
            )

    def update(self):
        super().update()
        self.update_stamina()
        self.update_saturation()
        self.update_energy()
        self.update_temperature()
    
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