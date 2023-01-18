import pygame as pg
from item_container import *
from crafting import *


SLOT_POS = 45, 45


class Inventory (ItemContainer):

    def __init__(self, slots, parent):
        self.parent = parent
        self.expanded = False

        img = self.texture_container.get(SLOT_DEFAULT)
        super().__init__(slot_img=img, slots=slots)
        self.setup_slots_positions( offset=(0, 120) )
        
        self.slot_index = 0
        self.dragging_slot = {}
        self.hover_slot = {}

        self.crafting = Crafting(self)

    @property
    def font(self):
        return self.texture_container.inventory_font

    @property
    def selected_slot(self):
        return self[self.slot_index]

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
    def data(self):
        return {
            "slot_index": self.slot_index,
            "slots": self.slots_data
        }

    def add_item(self, item):
        self.add(item.data)

    def pop_item(self, dropall, slot):
        slot = slot if slot else self.selected_slot

        if not slot:
            return
        
        return self.remove(slot) if dropall else self.pop(slot)

    def draw_small(self, screen):
        self.selected_slot.draw(screen, self.texture_container, SLOT_POS)
        
        slot_num = self.slot_index + 1
        w, h = self.selected_slot.rect.size
        slot_num_position = SLOT_POS[0] + w // 2 - SCALE, SLOT_POS[1] - h // 2 + SCALE

        screen_print(screen, slot_num, self.font, colors=(WHITE, LIGHT_GRAY), topleft=slot_num_position)

    def draw_dragging_item(self, screen):
        if not self.mouse_keys[0] or not self.dragging_slot:
            return

        item_texture = self.dragging_slot.get_item_texture(self.texture_container)
        item_rect = item_texture.get_rect(center=self.mouse_pos)
        screen.blit(item_texture, item_rect)
    
    def draw(self, screen):
        self.crafting.draw(screen)

        if self.expanded:
            super().draw(screen, self.texture_container)
            self.draw_dragging_item(screen)
        else:
            self.draw_small(screen)
    
    def get_input(self, events):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_keys = pg.mouse.get_pressed()
        
        for ev in events:
            if ev.type == pg.MOUSEWHEEL and not self.expanded:
                self.scroll(ev.y)

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_e:
                    self.toggle_expand()

            elif ev.type == pg.MOUSEBUTTONDOWN and self.expanded:
                if ev.button == pg.BUTTON_LEFT:
                    self.start_dragging()

            elif ev.type == pg.MOUSEBUTTONUP and self.expanded:
                if ev.button == pg.BUTTON_LEFT:
                    self.stop_dragging()
                
            elif ev.type == pg.MOUSEMOTION and self.expanded:
                self.update_hover_slot()

    def clear_crafting(self):
        for slot in self.crafting.slots:
            if not slot:
                continue

            try:
                self.add(slot)
            except ContainerFull:
                self.player.drop_item(dropall=True, slot=slot)
                
            slot.clear()
            
        self.crafting.output_slot.clear()

    def scroll(self, dif):
        if self.player.target:
            return
        
        num_of_slots = len(self)
        self.slot_index = (self.slot_index + dif) % num_of_slots

    def toggle_expand(self):
        if self.expanded:
            self.clear_crafting()
            self.dragging_slot = {}
            self.hover_slot = {}
        
        self.expanded = not self.expanded
        self.player.stop_moving()
        self.player.stop_action()
    
    def update_hover_slot(self):
        all_slots = self.slots + self.crafting.slots + [self.crafting.output_slot]

        for slot in all_slots:
            if slot.collidepoint(self.mouse_pos):
                self.hover_slot = slot
                return
        
        self.hover_slot = {}
        
    def start_dragging(self):
        all_slots = self.slots + self.crafting.slots + [self.crafting.output_slot]

        for slot in all_slots:
            if slot.collidepoint(self.mouse_pos):
                self.dragging_slot = slot
                return
            
        self.dragging_slot = {}

    def stop_dragging(self):
        if not self.dragging_slot:
            return
        
        slots = self.slots + self.crafting.slots

        if self.dragging_slot is self.crafting.output_slot:
            self.crafting.output_taken()
        
        for slot in slots:
            if slot.collidepoint(self.mouse_pos):
                if self.dragging_slot is self.crafting.output_slot and slot:
                    self.add(self.dragging_slot)
                else:
                    self.move_slot(self.dragging_slot, slot)
                
                self.dragging_slot = {}
                break
        else:
            self.player.drop_item(dropall=True, slot=self.dragging_slot)

        self.crafting.update()