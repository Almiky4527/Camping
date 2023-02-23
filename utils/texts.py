try:
    from .identifiers import *
except ImportError:
    from identifiers import *


# Text to display for entires that have no text.
PLACEHOLDER_TEXT = "???"


# --- Languages ---
EN = "English"
SK = "Slovenský"
LANGUAGES = [EN, SK]
# -----------------


# --- Texts ---
TEXTS = {
    EN: {
        "names": {
            ITEM_LOG: "Log of Wood",
            ITEM_STICK: "Wooden Stick",
            ITEM_AXE: "Axe",
            ITEM_TENT: "Tent",
            ITEM_MATCHES: "Matches",
            ITEM_CAMPFIRE: "Campfire",

            ITEM_CABIN_PLAN: "Cabin Plan",

            ROCK0: "Rock",
            ROCK1: "Rock",
            ROCK2: "Rock",
            ROCK3: "Rock",
            ROCK4: "Rock",
            STONE: "Stone",

            ITEM_BERRIES0: "Berries",
            ITEM_BLUEBERRIES: "Wild Blueberries",

            ITEM_PLANT0: "Plant",
            ITEM_PLANT1: "Plant",
            ITEM_PLANT2: "Plant",
            ITEM_PLANT3: "Parched Plant",

            ITEM_THREAD: "Thread",
            ITEM_ROPE: "Rope",
            ITEM_JACKET: "Jacket",
            ITEM_HAT: "Hat",

            ENTITY_CAMPFIRE: "Campfire",
            ENTITY_TENT: "Tent",

            BUSH_LARGE: "Large Bush",
            BUSH_SMALL: "Small Bush",

            ITEM_HARE_MEAT: "Hare Meat",
            ITEM_HARE_MEAT_COOKED: "Coodek Hare Meat",
            ITEM_HARE_HIDE: "Hare Hide",
            ITEM_DEER_MEAT: "Deer Meat",
            ITEM_DEER_MEAT_COOKED: "Cooked Deer Meat",
            ITEM_DEER_HIDE: "Deer Hide",
            ITEM_WOLF_MEAT: "Wolf Meat",
            ITEM_WOLF_MEAT_COOKED: "Cooked Wolf Meat",
            ITEM_WOLF_HIDE: "Wolf Hide",

            ITEM_4D617877656C6C: "Maxwell",
        },
        "legends": {
            ITEM_LOG: "Good for fire or building.",
            ITEM_STICK: "A great crafting ingredient.",
            ITEM_AXE: "A tool, but also a weapon.",
            ITEM_TENT: "Temporary shelter for your journeys.",
            ITEM_MATCHES: "Something to start the fire with.",
            ITEM_CAMPFIRE: "Essential for your survival.",

            ITEM_CABIN_PLAN: "100 Logs, 50 Sticks, 20 Ropes, 20 Rocks.",

            ROCK0: "A great crafting ingredient.",
            ROCK1: "A great crafting ingredient.",
            ROCK2: "Hides no secret...",
            ROCK3: "A great crafting ingredient.",
            ROCK4: "A great crafting ingredient.",
            STONE: "Or a pebble.",
            
            ITEM_BERRIES0: "A light source of food.",
            ITEM_BLUEBERRIES: "A light source of food.",

            ITEM_PLANT0: "A great crafting ingredient.",
            ITEM_PLANT1: "A great crafting ingredient.",
            ITEM_PLANT2: "A great crafting ingredient.",
            ITEM_PLANT3: "A great crafting ingredient.",

            ITEM_THREAD: "A great crafting ingredient.",
            ITEM_ROPE: "Crafting ingredient, building materail.",
            ITEM_JACKET: "Keeps you warm in cold weather.",
            ITEM_HAT: "Keeps you warm in cold weather.",

            ITEM_HARE_MEAT: "Needs to be cooked before eating.",
            ITEM_HARE_MEAT_COOKED: "A better food source.",
            ITEM_HARE_HIDE: "Can be used to make a hat.",
            ITEM_DEER_MEAT: "Needs to be cooked before eating.",
            ITEM_DEER_MEAT_COOKED: "A great food source.",
            ITEM_DEER_HIDE: "Can be used to make a coat.",
            ITEM_WOLF_MEAT: "Needs to be cooked before eating.",
            ITEM_WOLF_MEAT_COOKED: "A great food source.",
            ITEM_WOLF_HIDE: "Can be used to make a coat.",

            ITEM_4D617877656C6C: "My beloved.",
        },
        "world": {
            SEASON_SPRING: "Spring",
            SEASON_SUMMER: "Summer",
            SEASON_AUTUMN: "Autumn",
            SEASON_WINTER: "Winter",

            "info_text": "{season}, day {day}"
        },
        "menu": {
            "main": {
                "title": "CAMPING",
                "buttons": [
                    "C - Continue",
                    "N - New Game",
                    "W - Worlds  ",
                    "S - Settings",
                    "Q - Quit    "
                ],
                "loading_save": "Loading last played world...",
                "loading_new": "Generating new world..."
            },
            "select_character": {
                "title": "Select character",
                "M": "M - Male",
                "F": "F - Female"
            },
            "worlds": {
                "load": "Loading world...",
                "delete": "{world} deleted.",
                "empty": " Empty ",
                "buttons": [
                    "UP/DOWN - Scroll Worlds",
                    "ENTER - Play World     ",
                    "DEL - Delete World     ",
                    "ESC - Back to Main Menu"
                ]
            },
            "settings": {
                "lang_changed": "Changed language to {lang}.",
                "fullscreen": [
                    "Fullscreen OFF.",
                    "Fullscreen ON."
                ],
                "debug": [
                    "Debug mode OFF.",
                    "Debug mode ON."
                ],
                "shadows": [
                    "Shadow rendering OFF.",
                    "Shadow rendering ON."
                ],
                "buttons": [
                    "L - Change Language      ",
                    "F - Toggle Fullscreen    ",
                    "D - Toggle Debug Mode    ",
                    "S - Toggle Render Shadows",
                    "ESC - Back to Main Menu  "
                ]
            },
            "paused": {
                "title": "PAUSED",
                "buttons": [
                    "M - Return to Main Menu",
                    "D - Toggle Debug Mode  ",
                    "ESC - Resume",
                    "Q - Quit"
                ]
            },
            "new_day_loading": {
                "continue": "Press any key to continue.",
                "tips": [
                    "Consider resting after finishing some demanding actions.",
                    "Food can disappear when left out in the open over night.",
                    "Make sure to remember your way back home."
                ]
            }
        },
        "actions": {
            "save": {
                "q": "Skip to next day? y/n",
                "y": "Game state saved.",
                "n": "Saving canceled.",
                "x": "You cannot skip to next day right now."
            },
            "tired": "You are too tired to continue.",
            "energy_low": "You feel like you're going to pass out soon.",
            "inventory_full": "Your inventory is full.",
            "fire": {
                "lit": "You lit the {target} using your {item}.",
                "already_lit": "The {target} is already lit.",
                "fail": "You struck your {item} but nothing happended.",
                "feed": "You put {item} on the fire.",
                "no_feed": "There is no need to feed the fire right now.",
                "inspect": [
                    "The fire is in a great condition.",
                    "The fire could use a couple of logs.",
                    "The fire is almost burnt out."
                ]
            },
            "loot": {
                "search": "You search the {target}..."
            },
            "place": {
                "success": "You placed down a {thing}.",
                "fail": "You cannot place that here right now."
            },
            "eat": {
                "success": "You ate some delicious {food}.",
                "fail": "You aren't hungry enough to eat this right now."
            }
        }
    },
    SK: {
        "names": {
            ITEM_LOG: "Poleno Dreva",
            ITEM_STICK: "Drevená Palica",
            ITEM_AXE: "Sekera",
            ITEM_TENT: "Stan",
            ITEM_MATCHES: "Zápalky",
            ITEM_CAMPFIRE: "Táborák",

            ITEM_CABIN_PLAN: "Plán Zrubu",

            ROCK0: "Kameň",
            ROCK1: "Kameň",
            ROCK2: "Kameň",
            ROCK3: "Kameň",
            ROCK4: "Kameň",
            STONE: "Kamienok",

            ITEM_BERRIES0: "Bobule",
            ITEM_BLUEBERRIES: "Divoké Čučoriedky",

            ITEM_PLANT0: "Rastlina",
            ITEM_PLANT1: "Rastlina",
            ITEM_PLANT2: "Rastlina",
            ITEM_PLANT3: "Vysušená Rastlina",

            ITEM_THREAD: "Niť",
            ITEM_ROPE: "Lano",
            ITEM_JACKET: "Kabát",
            ITEM_HAT: "Čapica",

            ENTITY_CAMPFIRE: "Táborák",
            ENTITY_TENT: "Stan",

            BUSH_LARGE: "Veľký Ker",
            BUSH_SMALL: "Malý Ker",

            ITEM_HARE_MEAT: "Králičia Mäso",
            ITEM_HARE_MEAT_COOKED: "Uvarené Králičia Mäso",
            ITEM_HARE_HIDE: "Králičia Kožušina",
            ITEM_DEER_MEAT: "Jelenie Mäso",
            ITEM_DEER_MEAT_COOKED: "Uvarené Jelenie Mäso",
            ITEM_DEER_HIDE: "Jelenia Kožušina",
            ITEM_WOLF_MEAT: "Vlčie Mäso",
            ITEM_WOLF_MEAT_COOKED: "Uvarené Vlčie Mäso",
            ITEM_WOLF_HIDE: "Vlčia Kožušina",

            ITEM_4D617877656C6C: "Maxwell"
        },
        "legends": {
            ITEM_LOG: "Dobré na oheň alebo stavanie.",
            ITEM_STICK: "Skvelá prísada na tvorenie.",
            ITEM_AXE: "Nástroj, ale taktiež zbraň.",
            ITEM_TENT: "Dočasný prístrešok na tvoje cesty.",
            ITEM_MATCHES: "Hodia sa na založenie ohňa.",
            ITEM_CAMPFIRE: "Nevyhnutný na tvoje prežitie.",

            ITEM_CABIN_PLAN: "100 Polien, 50 Palíc, 20 Lán, 20 Kameňov.",

            ROCK0: "Skvelá prísada na tvorenie.",
            ROCK1: "Skvelá prísada na tvorenie.",
            ROCK2: "Neskrýva žiadnu tajnosť...",
            ROCK3: "Skvelá prísada na tvorenie.",
            ROCK4: "Skvelá prísada na tvorenie.",
            STONE: "Alebo okruhliak.",

            ITEM_BERRIES0: "Ľahký zdroj potravy.",
            ITEM_BLUEBERRIES: "Ľahký zdroj potravy.",

            ITEM_PLANT0: "Skvelá prísada na tvorenie.",
            ITEM_PLANT1: "Skvelá prísada na tvorenie.",
            ITEM_PLANT2: "Skvelá prísada na tvorenie.",
            ITEM_PLANT3: "Skvelá prísada na tvorenie.",

            ITEM_THREAD: "Skvelá prísada na tvorenie.",
            ITEM_ROPE: "Prísada na tvorenie, stavebný materiál.",
            ITEM_JACKET: "Udrží ťa v teple v chladnom počasí.",
            ITEM_HAT: "Udrží ťa v teple v chladnom počasí.",

            ITEM_HARE_MEAT: "Musí sa uvariť pred jedením.",
            ITEM_HARE_MEAT_COOKED: "Lepší zdroj potravy.",
            ITEM_HARE_HIDE: "Môže sa použiť na výrobu čapice.",
            ITEM_DEER_MEAT: "Musí sa uvariť pred jedením.",
            ITEM_DEER_MEAT_COOKED: "Skvelí zdroj potravy.",
            ITEM_DEER_HIDE: "Môže sa použiť na výrobu kabátu.",
            ITEM_WOLF_MEAT: "Musí sa uvariť pred jedením.",
            ITEM_WOLF_MEAT_COOKED: "Skvelí zdroj potravy.",
            ITEM_WOLF_HIDE: "Môže sa použiť na výrobu kabátu.",

            ITEM_4D617877656C6C: "Môj milovaný."
        },
        "world": {
            SEASON_SPRING: "Jar",
            SEASON_SUMMER: "Leto",
            SEASON_AUTUMN: "Jeseň",
            SEASON_WINTER: "Zima",

            "info_text": "{season}, deň {day}"
        },
        "menu": {
            "main": {
                "title": "KEMPOVAČKA",
                "buttons": [
                    "C - Pokračovať ",
                    "N - Nová Hra   ",
                    "W - Svety      ",
                    "S - Nastavenia ",
                    "Q - Opustiť Hru"
                ],
                "loading_save": "Načítavam posledne hraný svet...",
                "loading_new": "Vytváram nový svet..."
            },
            "select_character": {
                "title": "Vyber postavu",
                "M": "M - Muž",
                "F": "F - Žena"
            },
            "worlds": {
                "load": "Načítavam svet...",
                "delete": "{world} vymazaný.",
                "empty": "Prázdny",
                "buttons": [
                    "UP/DOWN - Rolovať Svetmi ",
                    "ENTER - Hrať Svet        ",
                    "DEL - Vymazať Svet       ",
                    "ESC - Späť na Hlavné Menu"
                ]
            },
            "settings": {
                "lang_changed": "Jazyk zmenený na {lang}.",
                "fullscreen": [
                    "Režim celej obrazovky VYPNUTÝ.",
                    "Režim celej obrazovky ZAPNUTÝ."
                ],
                "debug": [
                    "Režim ladenia VYPNUTÝ.",
                    "Režim ladenia ZAPNUTÝ."
                ],
                "shadows": [
                    "Vykreslovanie tieňov ZAPNUTÉ.",
                    "Vykreslovanie tieňov VYPNUTÉ."
                ],
                "buttons": [
                    "L - Zmeniť Jazyk                 ",
                    "F - Prepnúť Režim Celej Obrazovky",
                    "D - Prepnúť Režim Ladenia        ",
                    "S - Prepnúť vykreslovanie tieňov ",
                    "ESC - Späť na Hlavné Menu        "
                ]
            },
            "paused": {
                "title": "POZASTAVENÉ",
                "buttons": [
                    "M - Naspäť na Hlavné Menu",
                    "D - Prepnúť Režim Ladenia",
                    "ESC - Pokračovať",
                    "Q - Opustiť Hru"
                ]
            },
            "new_day_loading": {
                "continue": "Stlač ľubovoľnú klávesu pre pokračovanie.",
                "tips": [
                    "Zváž odpočinok po dokončení niektorých náročných akcií.",
                    "Jedlo môže zmiznúť keď ho necháš vonku cez noc.",
                    "Zapamätaj si cestu spät domov."
                ]
            }
        },
        "actions": {
            "save": {
                "q": "Preskočiť na ďalší deň? y/n",
                "y": "Stav hry uložený.",
                "n": "Ukladanie zrušené.",
                "x": "Teraz ešte nemôžeš preskočiť na ďalší deň."
            },
            "tired": "Si príliš vyčerpaný aby si pokračoval.",
            "energy_low": "Máš pocit že čoskoro omdlieš.",
            "inventory_full": "Tvoj inventár je plný.",
            "fire": {
                "lit": "Zapálil si {target} použitím {item}.",
                "already_lit": "{target} je už zapálený.",
                "fail": "Použil si svoje {item} ale nič sa nestalo.",
                "feed": "Položil si {item} na oheň.",
                "no_feed": "Nie je dôvod pridávať niečo na oheň v tejto chvíli.",
                "inspect": [
                    "Oheň je v perfeknej kondícii.",
                    "Oheň by mohol použiť zopár polienok.",
                    "Oheň je skoro vyhorený."
                ]
            },
            "loot": {
                "search": "Prehľadáš {target}..."
            },
            "place": {
                "success": "Rozložíš si {thing}.",
                "fail": "Toto tu nemôžeš rozložiť zrovna teraz."
            },
            "eat": {
                "success": "Zejdol si chutné {food}.",
                "fail": "Nie si dosť hladný aby si toto teraz zjedol."
            }
        }
    }
}
# -------------


# --- Functions ---

def get_text(lang, *args):
    value = TEXTS[lang]
    
    for key in args:
        if type(value) == dict:
            value = value.get(key)
        elif type(value) == list:
            value = value[key]
        else:
            return PLACEHOLDER_TEXT
    
    return value if type(value) == str else PLACEHOLDER_TEXT

def get_name(key, lang=EN):
    if lang not in LANGUAGES:
        return key

    return TEXTS[lang]["names"].get(key, key)

def get_legend(key, lang=EN):
    if lang not in LANGUAGES:
        return PLACEHOLDER_TEXT
    
    return TEXTS[lang]["legends"].get(key, PLACEHOLDER_TEXT)


def textify_data(data: dict):
    return [ f"{key}: {value}" for key, value in data.items() ]

# -----------------


if __name__ == "__main__":
    text = "{name} x {count}"
    print(text.format(name="Log", count=1))