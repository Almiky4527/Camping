from utils.identifiers import *


ITEMS = {
    ITEM_DEFAULT: {
        "family": ["item"],
        "max_count": 1
    },
    ITEM_LOG: {
        "family": ["item", "fire_fuel"],
        "fire_fuel": 20,
        "max_count": 4
    },
    ITEM_STICK: {
        "family": ["item", "fire_fuel"],
        "fire_fuel": 5,
        "max_count": 16
    },
    ITEM_AXE: {
        "family": ["item", "axe", "weapon"],
        "max_count": 1,
        "attack_damage": 30
    },
    ITEM_TENT: {
        "family": ["item", "spawn"],
        "spawn": ENTITY_TENT,
        "max_count": 1
    },
    ITEM_CAMPFIRE: {
        "family": ["item", "spawn"],
        "spawn": ENTITY_CAMPFIRE,
        "max_count": 1
    },
    ITEM_CABIN_PLAN: {
        "family": ["item", "spawn", "plan", "cabin"],
        "spawn": ENTITY_CABIN_FOUNDATION,
        "max_count": 3
    },
    ITEM_MATCHES: {
        "family": ["item", "fire_starter"],
        "success_chance": 0.7,
        "max_count": 32
    },
    ITEM_BERRIES0: {
        "family": ["item", "food", "berries"],
        "food": 5,
        "max_count": 64
    },
    ITEM_BLUEBERRIES: {
        "family": ["item", "food", "berries"],
        "food": 5,
        "max_count": 64
    },
    ITEM_PLANT0: {
        "family": ["item", "item_plant", "thread_maker"],
        "max_count": 32
    },
    ITEM_PLANT1: {
        "family": ["item", "item_plant", "thread_maker"],
        "max_count": 32
    },
    ITEM_PLANT2: {
        "family": ["item", "item_plant", "thread_maker"],
        "max_count": 32
    },
    ITEM_PLANT3: {
        "family": ["item", "item_plant", "thread_maker"],
        "max_count": 32
    },
    ROCK2: {
        "family": ["item", "cookable"],
        "cooking_gives": ITEM_4D617877656C6C,
        "max_count": 1
    },
    STONE: {
        "family": ["item", "stone"],
        "max_count": 8
    },
    ITEM_THREAD: {
        "family": ["item", "thread"],
        "max_count": 32
    },
    ITEM_ROPE: {
        "family": ["item", "rope"],
        "max_count": 20
    },
    ITEM_JACKET: {
        "family": ["item", "wearable", "jacket"],
        "warmth": 0.6,
        "max_count": 1
    },
    ITEM_HAT: {
        "family": ["item", "wearable", "hat"],
        "warmth": 0.2,
        "max_count": 1
    },
    ITEM_HARE_MEAT: {
        "family": ["item", "meat", "cookable"],
        "cooking_gives": ITEM_HARE_MEAT_COOKED,
        "max_count": 16
    },
    ITEM_HARE_MEAT_COOKED: {
        "family": ["item", "food", "meat"],
        "food": 15,
        "max_count": 16
    },
    ITEM_HARE_HIDE: {
        "family": ["item", "hide", "hare_hide"],
        "max_count": 16
    },
    ITEM_ROCK_TRAP: {
        "family": ["item"],
        "max_count": 1
    },
    ITEM_ROCK_TRAP_PRIMED: {
        "family": ["item", "spawn", "trap", "rock_trap"],
        "spawn": ENTITY_ROCK_TRAP,
        "max_count": 1
    },
    ITEM_NOOSE_TRAP: {
        "family": ["item", "spawn", "trap", "noose_trap"],
        "spawn": ENTITY_NOOSE_TRAP,
        "max_count": 1
    },
    ITEM_BOW: {
        "family": ["item", "bow", "projectile_shooter"],
        "ammunition": ITEM_ARROW,
        "max_count": 1
    },
    ITEM_ARROW: {
        "family": ["item", "arrow", "projectile_item"],
        "projectile": ENTITY_ARROW,
        "max_count": 10
    },
    ITEM_SPAWN_HARE: {
        "family": ["item", "spawn"],
        "spawn": ANIMAL_HARE,
        "max_count": 1
    },
    ITEM_SPAWN_BEAR: {
        "family": ["item", "spawn"],
        "spawn": ANIMAL_BEAR,
        "max_count": 1
    },
    ITEM_4D617877656C6C: {
        "family": ["item", "cat"],
        "max_count": 1
    }
}


ENTITIES = {
    ENTITY_DEFAULT: {
        "max_health": 100,
        "max_speed": 2,

        "box_size": [26, 9],

        "health": 100,
        "speed": 2,
        "attack_damage": 0,
        "attack_cooldown": 0.5,

        "loot": None,
        "immobile": True
    },
    ENTITY_PLAYER: {
        "family": ["player", "small"],
        "max_health": 100,
        "max_speed": 3,

        "box_size": [10, 2],
        "reach_size": [20, 10],

        "temperature": 37,

        "health": 100,
        "speed": 2,
        "stamina": 100,
        "saturation": 100,
        "attack_damage": 10,
        "attack_cooldown": 0.5
    },
    ENTITY_TENT: {
        "family": ["tent", "bed", "savepoint"],

        "box_size": [54, 12],
        "immobile": True
    },
    ENTITY_CAMPFIRE: {
        "family": ["campfire"],
        
        "saturation": 0,

        "box_size": [18, 6],
        "immobile": True
    },
    ENTITY_CABIN_FOUNDATION: {
        "family": ["cabin", "foundation"],
        "required_build_materials": [
            [ [ITEM_LOG], 100 ],
            [ [ITEM_STICK], 50 ],
            [ [ITEM_ROPE], 20 ],
            [ [ROCK0, ROCK1, ROCK2, ROCK3, ROCK4], 20 ]
        ],
        "output_building": ENTITY_CABIN,
        "box_size": [62, 20],
        "immobile": True
    },
    ENTITY_CABIN: {
        "family": ["cabin", "savepoint", "building"],
        "cold_protection": True,
        "box_size": [62, 20],
        "immobile": True
    },
    PINE_SMALL: {
        "family": ["foliage", "tree", "pine", "small"],
        "max_health": 300,
        "health": 300,

        "box_size": [4, 2],
        "immobile": True,
        "loot": {
            ITEM_LOG: 2,
            ITEM_STICK: [0, 2]
        }
    },
    PINE_LARGE: {
        "family": ["foliage", "tree", "pine", "large"],
        "max_health": 500,
        "health": 500,

        "box_size": [4, 2],
        "immobile": True,
        "loot": {
            ITEM_LOG: [3, 4],
            ITEM_STICK: [0, 3]
        }
    },
    OAK_SMALL: {
        "family": ["foliage", "tree", "oak", "small"],
        "max_health": 300,
        "health": 300,

        "box_size": [4, 2],
        "immobile": True,
        "loot": {
            ITEM_LOG: 2,
            ITEM_STICK: [0, 2]
        }
    },
    OAK_LARGE: {
        "family": ["foliage", "tree", "oak", "large"],
        "max_health": 500,
        "health": 500,

        "box_size": [4, 2],
        "immobile": True,
        "loot": {
            ITEM_LOG: [3, 4],
            ITEM_STICK: [0, 3]
        }
    },
    BUSH_LARGE: {
        "family": ["foliage", "bush", "large", "interact_loot", "loot"],
        "max_health": 50,
        "health": 50,

        "interact_loot": {
            ITEM_BERRIES0: [2, 5]
        },
        "looting_time": 4,

        "immobile": True,
        "loot": {
            ITEM_STICK: [1, 4]
        }
    },
    BUSH_SMALL: {
        "family": ["foliage", "bush", "small", "interact_loot", "loot"],
        "max_health": 30,
        "health": 30,

        "interact_loot": {
            ITEM_BLUEBERRIES: [1, 3]
        },
        
        "looting_time": 2,

        "immobile": True,
        "loot": {
            ITEM_STICK: [1, 3],
        }
    },
    PLANT0: {
        "family": ["plant"],
        "max_health": 10,
        "health": 10,

        "immobile": True,
        "loot": {
            ITEM_PLANT0: 1
        }
    },
    PLANT1: {
        "family": ["plant"],
        "max_health": 10,
        "health": 10,

        "immobile": True,
        "loot": {
            ITEM_PLANT1: 1
        }
    },
    PLANT2: {
        "family": ["plant"],
        "max_health": 10,
        "health": 10,

        "immobile": True,
        "loot": {
            ITEM_PLANT2: 1
        }
    },
    PLANT3: {
        "family": ["plant", "parched"],
        "max_health": 10,
        "health": 10,

        "immobile": True,
        "loot": {
            ITEM_PLANT3: 1
        }
    },
    ANIMAL_HARE: {
        "family": ["animal", "hare", "small"],
        "max_health": 50,
        "max_speed": 3,
        "default_speed": 2,
        "reach_size": [10, 5],
        "health": 50,
        "speed": 2,
        "attack_damage": 10,
        "attack_cooldown": 0.1,
        "max_travel_dist": 200,
        "travel_chance": 0.005,
        "run_away_from": [
            {
                "family": "player",
                "see_dist": 200,
                "run_dist": 1
            }
        ],
        "possible_targets": [
            {
                "family": "hare_lure",
                "see_dist": 400,
                "forget_dist": 500
            }
        ],
        "loot": {
            ITEM_HARE_MEAT: 1,
            ITEM_HARE_HIDE: 1
        }
    },
    ANIMAL_DEER: {
        "family": ["animal", "deer", "large"],
        "max_health": 100,
        "max_speed": 4,
        "default_speed": 1,
        "health": 100,
        "speed": 2,
        "reach_size": [20, 10],
        "max_travel_dist": 300, # 300
        "travel_chance": 0.001,
        "run_away_from": [
            {
                "family": "player",
                "see_dist": 300, # 300
                "run_dist": 2
            }
        ],
        "loot": {
            ITEM_DEER_MEAT: 1,
            ITEM_DEER_HIDE: 1
        }
    },
    ANIMAL_WOLF: {
        "family": ["animal", "wolf"],
        "max_health": 100,
        "max_speed": 4,
        "default_speed": 1,
        "reach_size": [30, 20],
        "health": 100,
        "speed": 1,
        "attack_damage": 25,
        "attack_cooldown": 0.5,
        "max_travel_dist": 600,
        "travel_chance": 0.001,
        "possible_targets": [
            {
                "family": "hare",
                "see_dist": 400,
                "forget_dist": 500
            }
        ]
    },
    ANIMAL_BEAR: {
        "family": ["animal", "bear"],
        "max_health": 300,
        "max_speed": 2,
        "default_speed": 1,
        "reach_size": [30, 20],
        "health": 300,
        "speed": 1,
        "attack_damage": 40,
        "attack_cooldown": 1.0,
        "max_travel_dist": 600,
        "travel_chance": 0.0008,
        "possible_targets": [
            {
                "family": "player",
                "see_dist": 200,
                "forget_dist": 400
            }
        ]
    },
    ENTITY_ROCK_TRAP: {
        "family": ["trap", "rock_trap", "hare_lure"],
        "max_health": 1,
        "max_speed": 0,
        "default_speed": 0,
        "health": 1,
        "reach_size": [10, 5],
        "speed": 0,
        "attack_damage": 50,
        "attack_cooldown": 0.1,
        "possible_targets": [
            {
                "family": "hare",
                "see_dist": 20,
                "forget_dist": 30
            }
        ],
        "loot": {
            ITEM_ROCK_TRAP: 1
        }
    },
    ENTITY_NOOSE_TRAP: {
        "family": ["trap", "noose_trap", "die_on_attack"],
        "max_health": 1,
        "max_speed": 0,
        "default_speed": 0,
        "health": 1,
        "reach_size": [16, 5],
        "speed": 0,
        "attack_damage": 50,
        "attack_cooldown": 0.05,
        "possible_targets": [
            {
                "family": "hare",
                "see_dist": 20,
                "forget_dist": 30
            }
        ],
        "loot": {
            ITEM_STICK: [1, 2],
            ITEM_THREAD: [0, 1]
        }
    },
    ENTITY_ARROW: {
        "family": ["arrow", "projectile", "die_on_attack"],
        "max_health": 1,
        "max_speed": 2,
        "default_speed": 2,
        "health": 1,
        "reach_size": [16, 5],
        "speed": 2,
        "attack_damage": 50,
        "attack_cooldown": 0.01,
        "projectile_item": ITEM_ARROW
    },
}


def entity_subtype(entity_id):
    if not entity_id:
        return 

    return entity_id.split('.')[0]


def item(item_id, count=1):
    item_data = ITEMS.get(item_id, ITEMS[ITEM_DEFAULT]).copy()

    max_count = item_data["max_count"]
    count = max_count if count > max_count else 1 if count <= 0 else count

    item_data["id"] = item_id
    item_data["count"] = count
    return item_data


def entity(entity_id):
    entity_data = ENTITIES.get( entity_id, ENTITIES[ENTITY_DEFAULT] ).copy()

    if entity_subtype(entity_id) == "item" and not entity_data.get("count"):
        entity_data["count"] = 1

    entity_data["id"] = entity_id
    return entity_data