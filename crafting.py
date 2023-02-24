import pygame as pg
from item_container import *
from entities import *
from utils.display import *


RECIPES = [
    {
        "result": ITEM_CAMPFIRE,
        "ingredients": [
            [ITEM_LOG, 1],
            [ITEM_STICK, 3]
        ]
    },
    {
        "result": ITEM_THREAD,
        "ingredients": [
            [ [ITEM_PLANT0, ITEM_PLANT1, ITEM_PLANT2, ITEM_PLANT3], 3 ]
        ]
    },
    {
        "result": ITEM_ROPE,
        "ingredients": [
            [ITEM_THREAD, 6]
        ]
    },
    {
        "result": ITEM_JACKET,
        "ingredients": [
            [ITEM_DEER_HIDE, 1],
            [ITEM_THREAD, 20]
        ]
    },
    {
        "result": ITEM_HAT,
        "ingredients": [
            [ITEM_HARE_HIDE, 2],
            [ITEM_THREAD, 10]
        ]
    },
    {
        "result": ITEM_ROCK_TRAP,
        "ingredients": [
            [ITEM_STICK, 1],
            [ [ROCK0, ROCK1, ROCK2, ROCK3, ROCK4], 1 ]
        ]
    },
    {
        "result": ITEM_ROCK_TRAP_PRIMED,
        "ingredients": [
            [ITEM_ROCK_TRAP, 1],
            [ [ITEM_BERRIES0, ITEM_BLUEBERRIES], 1 ]
        ]
    },
    {
        "result": ITEM_NOOSE_TRAP,
        "ingredients": [
            [ITEM_STICK, 2],
            [ITEM_THREAD, 1]
        ]
    }
]


class Crafting (ItemContainer):

    def __init__(self, parent):
        self.parent = parent

        img_plus = self.texture_container.get(SLOT_PLUS)
        super().__init__(slot_img=img_plus, slots=[ {} for _ in range(3) ] )
        self.setup_slots_positions( offset=(0, -75) )
        
        img_equals = self.texture_container.get(SLOT_EQUALS)
        output_slot_position = SCREEN_CENTER[0], SCREEN_CENTER[1] - 205
        self.output_slot = ItemSlot(img_equals, {}, output_slot_position)

        self.recipe_in_use = {}
    
    @property
    def font(self):
        return self.texture_container.inventory_font

    @property
    def player(self):
        return self.parent.player

    @property
    def world(self):
        return self.parent.world

    @property
    def texture_container(self):
        return self.parent.texture_container
    
    @property
    def expanded(self):
        return self.parent.expanded
    
    def matches_recipe(self, recipe):
        ingredients = recipe["ingredients"]

        num_of_checks = 0
        required_checks = len(ingredients)

        for required_item_s, required_count in ingredients:
            for slot in self.slots:
                if not slot:
                    continue

                item_id, count =  slot["id"], slot["count"]

                if item_id in required_item_s and count >= required_count:
                    num_of_checks += 1
                    break
        
        return num_of_checks == required_checks
    
    def update(self):
        for recipe in RECIPES:
            if self.matches_recipe(recipe):
                item_id = recipe["result"]
                self.output_slot.update( item(item_id) )
                self.recipe_in_use = recipe
                break
        else:
            self.output_slot.clear()
            self.recipe_in_use = {}
    
    def output_taken(self):
        input_ingredients = self.recipe_in_use["ingredients"]

        for required_item_id_s, required_count in input_ingredients:
            for slot in self.slots:
                if not slot:
                    continue

                if slot["id"] in required_item_id_s:
                    self.pop_more(slot, required_count)
                    break
    
    def draw(self, screen):
        if self.expanded:
            super().draw(screen, self.texture_container)
            self.output_slot.draw(screen, self.texture_container)