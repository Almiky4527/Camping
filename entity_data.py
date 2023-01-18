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
        "attack_damage": 30 # 30
    },
    ITEM_TENT: {
        "family": ["item", "spawn"],
        "spawn": ENTITY_TENT,
        "max_count": 1
    },
    ITEM_CAMPFIRE: {
        "family": ["item", "spawn"],
        "spawn": ENTITY_CAMPFIRE,
        "max_count": 2
    },
    ITEM_MATCHES: {
        "family": ["item", "fire_starter"],
        "success_chance": 0.7,
        "max_count": 32
    },
    ITEM_BERRIES0: {
        "family": ["item", "food", "berries"],
        "food": 10,
        "max_count": 16
    },
    ITEM_BLUEBERRIES: {
        "family": ["item", "food", "berries"],
        "food": 12,
        "max_count": 16
    },
    ITEM_PLANT0: {
        "family": ["item", "thread_maker"],
        "max_count": 16
    },
    ITEM_PLANT1: {
        "family": ["item", "thread_maker"],
        "max_count": 16
    },
    ITEM_PLANT2: {
        "family": ["item", "thread_maker"],
        "max_count": 16
    },
    ITEM_PLANT3: {
        "family": ["item", "thread_maker"],
        "max_count": 16
    },
    ITEM_THREAD: {
        "family": ["item", "thread"],
        "max_count": 32
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
        "family": ["foliage", "bush", "large", "interact", "loot"],
        "max_health": 50,
        "health": 50,

        "interact_loot": {
            ITEM_BERRIES0: [2, 5]
        },
        "looting_time": 5,

        "immobile": True,
        "loot": {
            ITEM_STICK: [1, 4]
        }
    },
    BUSH_SMALL: {
        "family": ["foliage", "bush", "small", "interact", "loot"],
        "max_health": 30,
        "health": 30,

        "interact_loot": {
            ITEM_BLUEBERRIES: [1, 3]
        },
        
        "looting_time": 3,

        "immobile": True,
        "loot": {
            ITEM_STICK: [0, 3],
        }
    },
    PLANT0: {
        "family": ["plant"],
        "max_health": 20,
        "health": 20,

        "immobile": True,
        "loot": {
            ITEM_PLANT0: 1
        }
    },
    PLANT1: {
        "family": ["plant"],
        "max_health": 20,
        "health": 20,

        "immobile": True,
        "loot": {
            ITEM_PLANT1: 1
        }
    },
    PLANT2: {
        "family": ["plant"],
        "max_health": 20,
        "health": 20,

        "immobile": True,
        "loot": {
            ITEM_PLANT2: 1
        }
    },
    PLANT3: {
        "family": ["plant", "parched"],
        "max_health": 20,
        "health": 20,

        "immobile": True,
        "loot": {
            ITEM_PLANT3: 1
        }
    }
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