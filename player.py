import pygame as pg
from random import randrange, random
from settings import *
from items import *
from terrain import *
from inventory import *


class Player (Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.direction = pg.math.Vector2()
        self.speed = 2
        self.reach = pg.Rect(0, 0, 60, 20)

        self.action_actor = None
        self.action_pos = None

    @property
    def world(self):
        return self.parent.world

    @property
    def camera(self):
        return self.parent.camera

    @property
    def inventory(self):
        return self.parent.inventory

    @property
    def selected_slot(self):
        return self.inventory.selected_slot

    @property
    def can_cut_tree(self):
        return self.selected_slot["iid"] == AXE if self.selected_slot else False

    @property
    def is_cutting_tree(self):
        return type(self.action_actor) == Tree and self.in_reach(self.action_pos)

    def stop_action(self):
        self.action_actor = None
        self.action_pos = None

    def collision(self, obj):
        return obj.box.collidepoint(self.position)

    def in_reach(self, position):
        return self.reach.collidepoint(position) if position else False

    def move(self):
        self.box.midbottom += self.direction * self.speed

    def get_input(self, events):
        keys = pg.key.get_pressed()

        if keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            self.stop_action()

        if keys[pg.K_a] and keys[pg.K_d]:
            self.direction.x = 0
        elif keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pg.K_w] and keys[pg.K_s]:
            self.direction.y = 0
        elif keys[pg.K_w]:
            self.direction.y = -1
        elif keys[pg.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_LSHIFT]:
            self.speed = 3
        else:
            self.speed = 2

        for ev in events:
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_q and keys[pg.K_LSHIFT]:
                    self.drop_item(dropall = True)
                elif ev.key == pg.K_q:
                    self.drop_item()

            elif ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button != pg.BUTTON_LEFT:
                    continue

                mouse_pos = pg.mouse.get_pos()
                self.action_pos = position_from_screen(mouse_pos, self.camera.topleft)

                for child in self.camera.scene:
                    if not child.box.collidepoint(self.action_pos) or child is self:
                        continue

                    if type(child) == Item:
                        pass
                    
                    elif type(child) == Tree:
                        if not self.can_cut_tree:
                            continue

                    self.action_actor = child
                    self.action_pos = child.position
                    break
                else:
                    self.action_actor = None
                    
    def pickup_item(self):
        item = self.action_actor
        self.inventory.add_item(item)
        self.stop_action()

    def drop_item(self, dropall=False, slot=None):
        self.inventory.pop_item(dropall, slot)
            
    def cutdown_tree(self):
        tree = self.action_actor
        tree.health -= 10

        if tree.health <= 0:
            self.stop_action()
            
    def move_to_action(self):
        if not self.action_pos:
            return
        elif self.in_reach(self.action_pos):
            self.direction = pg.math.Vector2()
            return

        vector = pg.math.Vector2(self.action_pos) - self.position
        vector.x = 0 if abs(vector.x) < 2 else vector.x
        vector.y = 0 if abs(vector.y) < 2 else vector.y
        direction = directionalize(vector)
        self.direction = direction

    def run_action(self):
        if not self.action_actor or not self.in_reach(self.action_pos):
            return

        if type(self.action_actor) == Item:
            self.pickup_item()
        elif type(self.action_actor) == Tree:
            self.cutdown_tree()
        else:
            pass

    def update(self):
        self.move_to_action()
        self.run_action()
        self.move()
        self.reach.center = self.position
