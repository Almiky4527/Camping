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
            [ITEM_PLANT0, 3]
        ]
    },
    {
        "result": ITEM_THREAD,
        "ingredients": [
            [ITEM_PLANT1, 3]
        ]
    },
    {
        "result": ITEM_THREAD,
        "ingredients": [
            [ITEM_PLANT2, 3]
        ]
    },
    {
        "result": ITEM_THREAD,
        "ingredients": [
            [ITEM_PLANT3, 3]
        ]
    },
    {
        "result": ITEM_ROPE,
        "ingredients": [
            [ITEM_THREAD, 6]
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

        for required_item, required_count in ingredients:
            for slot in self.slots:
                if not slot:
                    continue

                item_id, count =  slot["id"], slot["count"]

                if item_id == required_item and count >= required_count:
                    num_of_checks += 1
        
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

        for required_item_id, required_count in input_ingredients:
            for slot in self.slots:
                if not slot:
                    continue

                if slot["id"] == required_item_id:
                    self.pop_more(slot, required_count)
    
    def draw(self, screen):
        if self.expanded:
            super().draw(screen, self.texture_container)
            self.output_slot.draw(screen, self.texture_container)