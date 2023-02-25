from pygame import Surface

from entities import *
from utils.display import *
from utils.classes import ContainerFull


SLOT_DEFAULT = "slot.default"
SLOT_PLUS = "slot.splus"
SLOT_EQUALS = "slot.equals"
SLOT_WEAR_JACKET = "slot.wear.jacket"
SLOT_WEAR_HAT = "slot.wear.hat"


class ItemSlot:

    def __init__( self, image : Surface, data : dict, position=(0, 0) ):
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.data = data
    
    def __str__(self) -> str:
        return str(self.data)
    
    def __dict__(self) -> dict:
        return self.data.copy()

    def __bool__(self):
        return bool(self.data)
    
    def __eq__(self, __o: object) -> bool:
        return self.data == __o
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
    
    @property
    def is_empty(self):
        return bool(self) == False
    
    @property
    def position(self):
        return self.rect.center
    
    @property
    def family(self):
        return self.data.get( "family", () )

    @property
    def durability(self):
        return self.data.get("durability", None)
    
    def in_family(self, value : str):
        if not self.family:
            return False
        
        return value in self.family
    
    def get_item_texture(self, texture_container):
        if self.is_empty:
            return
        
        item_id = self.get("id")

        if not item_id:
            return
        
        return texture_container.get(item_id)

    def clear(self):
        self.data.clear()
    
    def copy(self):
        return self.data.copy()

    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def items(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()
    
    def update(self, E):
        self.data.update(E.data if type(E) == ItemSlot else E)
    
    def values(self):
        return self.data.values()
    
    def collidepoint(self, position):
        return self.rect.collidepoint(position)

    def set_position(self, position):
        self.rect.center = position
    
    def set_content(self, data : dict):
        self.data = data
    
    def set_durability(self, value : int):
        self.data["durability"] = max(0, value)
    
    def draw(self, screen, texture_container, position=None):
        if position:
            rect = self.rect.copy()
            rect.center = position
        else:
            rect = self.rect

        screen.blit(self.image, rect)

        if self.is_empty:
            return

        item_texture = self.get_item_texture(texture_container)
        item_rect = item_texture.get_rect(center=position if position else self.position)
        screen.blit(item_texture, item_rect)

        item_count = self.get("count")

        if not item_count or item_count == 1:
            return

        count_position = rect.x + SCALE, rect.y + SCALE
        screen_print(screen, item_count, texture_container.inventory_font, colors=(WHITE, LIGHT_GRAY), topleft=count_position)


class ItemContainer:

    def __init__(self, slot_img, slots : list):
        self.slots = [ ItemSlot(slot_img, slot_data) for slot_data in slots ]
    
    def __str__(self) -> str:
        return str( list( map(str, self.slots) ) )
    
    def __len__(self) -> int:
        return len(self.slots)
    
    def __contains__(self, item):
        if type(item) is Entity:
            return item.id in self.items
        return item in self.items
    
    def __getitem__(self, key):
        return self.slots[key]
    
    def __iter__(self):
        return iter(self.slots)
    
    @property
    def items(self):
        get_item_id = lambda slot : slot.get("id")
        return tuple( map(get_item_id, self.slots) )
    
    @property
    def slots_data(self):
        return [ dict(slot) for slot in self.slots ]
    
    @property
    def nonempty_slots(self):
        return tuple( filter(None, self.slots) )
    
    @property
    def empty_slots(self):
        is_empty = lambda slot : not slot
        return tuple( filter(is_empty, self.slots) )
    
    @property
    def is_full(self):
        return len(self.empty_slots) == 0
    
    def clear(self):
        for slot in self:
            slot.clear()
    
    def index(self, item : Entity | int):
        if type(item) == Entity:
            return self.items.index(item.id)
        return self.items.index(item)
    
    def move_slot(self, from_slot : ItemSlot, to_slot : ItemSlot):
        if from_slot is to_slot or from_slot.is_empty:
            return

        if from_slot.get("id") == to_slot.get("id"):
            self.merge_slot(from_slot.data, to_slot.data)
            return
        
        temp = to_slot.copy()
        to_slot.clear()
        to_slot.update(from_slot)
        from_slot.clear()
        from_slot.update(temp)
    
    def merge_slot(self, from_slot : ItemSlot, to_slot : ItemSlot):
        from_id, from_count = from_slot["id"], from_slot["count"]
        to_id, to_count = to_slot["id"], to_slot["count"]
        max_count = to_slot["max_count"]

        if to_id != from_id:
            return 
        
        remainder = max( (to_count + from_count) - max_count, 0 )
        addition = from_count - remainder

        to_slot["count"] += addition
        self.pop_more(from_slot, addition)
    
    def pop(self, slot : dict):
        if not slot:
            return {}

        copy = slot.copy()
        copy["count"] = 1
        
        if slot["count"] > 1:
            slot["count"] -= 1
        else:
            slot.clear()

        return copy
    
    def pop_more(self, slot : dict, amount : int):
        if not slot or amount <= 0 or amount > slot["count"]:
            return {}
        
        copy = slot.copy()
        copy["count"] = amount

        for _ in range(amount):
            self.pop(slot)

        return copy
    
    def add(self, item_data : dict):
        id_, count, max_count = item_data["id"], item_data["count"], item_data["max_count"]

        for non_empty_slot in self.nonempty_slots:
            if non_empty_slot["id"] != id_:
                continue

            if non_empty_slot["count"] + count > max_count:
                continue
            
            non_empty_slot["count"] += count
            return
        
        if self.is_full:
            raise ContainerFull("Inventory is full")
        
        self.empty_slots[0].set_content( item_data.copy() )

    def remove(self, slot : dict):
        copy = slot.copy()
        slot.clear()
        return copy
    
    def setup_slots_positions( self, offset=(0, 0) ):
        offset_x, offset_y = offset

        for i, slot in enumerate(self.slots):
            row, col = i // 3 - 1, i % 3 - 1
            w, h = slot.rect.size

            x = SCREEN_CENTER[0] + w * col + offset_x
            y = SCREEN_CENTER[1] + h * row + offset_y

            slot.set_position( (x, y) )

    def draw(self, screen, texture_container):
        for slot in self.slots:
            slot.draw(screen, texture_container)
