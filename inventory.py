import pygame as pg
from settings import *
from items import *


class Inventory:

    def __init__(self, parent):
        self.parent = parent
        self.slots = [ {} for _ in range(9) ]
        self.slot_index = 0
        
        self.expanded = False
        self.slot_rect = None
        self.slots_rects = []
        self.dragging_slot = None

        self.crafting_slots = [ {} for _ in range(3) ]
        self.crafting_output_slot = {}
        self.crafting_rects = []
        self.crafting_output_rect = None

        self.setup()

    def __contains__(self, item):
        if type(item) == Item:
            item = item.iid
        return item in self.items

    def __getitem__(self, key):
        return self.slots[key]

    def setup(self):
        slot_img = self.texture_container.inventory[SLOT]
        w, h = slot_img.get_size()
        self.slot_rect = slot_img.get_rect(center = SLOT_POS)
        
        for i, slot in enumerate(self.slots):
            row, col = i // 3 - 1, i % 3 - 1

            x = SCREEN_CENTER[0] + w * col
            y = SCREEN_CENTER[1] + h * row + 120
            
            rect = slot_img.get_rect( center = (x, y) )
            self.slots_rects.append(rect)

        for i, slot in enumerate(self.crafting_slots):
            col = i % 3 - 1

            x = SCREEN_CENTER[0] + w * col
            y = SCREEN_CENTER[1] + h - 205

            rect = slot_img.get_rect( center = (x, y) )
            self.crafting_rects.append(rect)

        pos = SCREEN_CENTER[0], SCREEN_CENTER[1] - 205
        self.crafting_output_rect = slot_img.get_rect(center = pos)

    def index(self, item):
        if type(item) == Item:
            item = item.iid
        return self.items.index(item)

    @property
    def font(self):
        return self.texture_container.inventory_font

    @property
    def selected_slot(self):
        return self[self.slot_index]

    @property
    def nonempty_slots(self):
        return list( filter(None, self.slots) )

    @property
    def items(self):
        return list( map(lambda slot : slot.get("iid"), self.slots) )

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
    def is_full(self):
        return len(self.nonempty_slots) == len(self.slots)

    def set_slot(self, index, iid, count):
        slot = self[index]
        slot["iid"] = iid
        slot["count"] = count

    def move_slot(self, from_slot, to_slot):
        temp = to_slot.copy()
        to_slot["iid"] = from_slot["iid"]
        to_slot["count"] = from_slot["count"]

        if temp:
            from_slot["iid"] = temp["iid"]
            from_slot["count"] = temp["count"]
        else:
            from_slot.clear()

    def clear_crafting(self):
        for slot in self.crafting_slots:
            if not slot:
                continue

            iid, count = slot["iid"], slot["count"]

            try:
                self.add(iid, count)
            except InventoryFull:
                self.pop_item(dropall = True, slot = slot)
                
            slot.clear()
            
        self.crafting_output_slot.clear()

    def add_item(self, item):
        try:
            self.add(item.iid, item.count)
            self.world.remove_child(item)
        except InventoryFull:
            print("Invenotry is full")
            
    def add(self, iid, count):
        for slot in self.nonempty_slots:
            if slot["iid"] == iid:
                max_count = MAX_COUNTS[iid]
                
                if slot["count"] >= max_count or slot["count"] + count > max_count:
                    continue
                
                slot["count"] += count
                break
        else:
            if self.is_full:
                raise InventoryFull("Inventory is full")
            
            for i, slot in enumerate(self.slots):
                if slot:
                    continue

                self.set_slot(i, iid, count)
                break

    def pop_item(self, dropall, slot):
        slot = slot if slot else self.selected_slot
        amount = -1 if dropall else 1
        
        iid, count = self.pop(slot, amount)

        if iid != None:
            self.world.spawn_item(iid, self.player.position, count)

    def pop(self, slot, amount):
        if not slot or amount < -1 or amount == 0:
            return None, None

        iid = slot["iid"]
        count = slot["count"]
        amount = count if amount > count or amount == -1 else amount

        slot["count"] -= amount

        if slot["count"] <= 0:
            slot.clear()

        return iid, amount

    def draw_small(self, screen):
        self.draw_slot(screen, SLOT, self.selected_slot, self.slot_rect)
        w, h = self.slot_rect.size
        pos = SLOT_POS[0] + w // 2 - SCALE, SLOT_POS[1] - h // 2 + SCALE
        print_(screen, self.slot_index + 1, self.font, WHITE, LIGHT_GRAY, topleft = pos)

    def draw_big(self, screen):
        for i, slot in enumerate(self.slots):
            rect = self.slots_rects[i]
            self.draw_slot(screen, SLOT, slot, rect)

    def draw_crafting(self, screen):
        for i, slot in enumerate(self.crafting_slots):
            rect = self.crafting_rects[i]
            self.draw_slot(screen, SLOT_PLUS, slot, rect)
            
        self.draw_slot(screen, SLOT_EQUALS, self.crafting_output_slot, self.crafting_output_rect)
            
    def draw_slot(self, screen, i, slot, rect):
        img = self.texture_container.inventory[i]
        screen.blit(img, rect)

        if not slot:
            return

        iid = slot["iid"]
        count = slot["count"]
        item_texture = self.texture_container.items[iid]
        item_rect = item_texture.get_rect(center = rect.center)
        screen.blit(item_texture, item_rect)

        if count == 1:
            return

        pos = rect.x + SCALE, rect.y + SCALE
        print_(screen, count, self.font, WHITE, LIGHT_GRAY, topleft = pos)
        

    def draw(self, screen):
        if self.expanded:
            self.draw_big(screen)
            self.draw_crafting(screen)
        else:
            self.draw_small(screen)

        if not self.expanded or not self.dragging_slot:
            return

        if self.mouse_keys[0]:
            iid = self.dragging_slot["iid"]
            item_texture = self.texture_container.items[iid]
            item_rect = item_texture.get_rect(center = self.mouse_pos)
            screen.blit(item_texture, item_rect)
        
    def get_input(self, events):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_keys = pg.mouse.get_pressed()
        
        for ev in events:
            if ev.type == pg.MOUSEWHEEL and not self.expanded:
                if self.player.action_actor:
                    continue
                
                self.slot_index += ev.y
                self.slot_index %= len(self.slots)

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_e:
                    self.expanded = not self.expanded

                    if not self.expanded:
                        self.clear_crafting()

            elif ev.type == pg.MOUSEBUTTONDOWN and self.expanded:
                if ev.button == pg.BUTTON_LEFT:
                    for i, rect in enumerate(self.slots_rects):
                        if not rect.collidepoint(self.mouse_pos):
                            continue
                        
                        self.dragging_slot = self.slots[i]
                        break
                    else:
                        for i, rect in enumerate(self.crafting_rects):
                            if not rect.collidepoint(self.mouse_pos):
                                continue
                            
                            self.dragging_slot = self.crafting_slots[i]
                            break
                        else:
                            self.dragging_slot = None

            elif ev.type == pg.MOUSEBUTTONUP and self.expanded:
                if ev.button == pg.BUTTON_LEFT:
                    if self.dragging_slot:
                        for i, rect in enumerate(self.slots_rects):
                            if not rect.collidepoint(self.mouse_pos):
                                continue
                            
                            slot = self.slots[i]
                            self.move_slot(self.dragging_slot, slot)
                            break
                        else:
                            for i, rect in enumerate(self.crafting_rects):
                                if not rect.collidepoint(self.mouse_pos):
                                    continue

                                slot = self.crafting_slots[i]
                                self.move_slot(self.dragging_slot, slot)
                                break
                            else:
                                self.pop_item(dropall = True, slot = self.dragging_slot)
                    
                        self.dragging_slot = None


class InventoryFull (Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
