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

            ROCK0: "Rock",
            ROCK1: "Rock",
            ROCK2: "Rock",
            ROCK3: "Rock",
            ROCK4: "Rock",

            ITEM_BERRIES0: "Berries",
            ITEM_BLUEBERRIES: "Wild Blueberries",

            ITEM_PLANT0: "Plant",
            ITEM_PLANT1: "Plant",
            ITEM_PLANT2: "Plant",
            ITEM_PLANT3: "Parched Plant",

            ENTITY_CAMPFIRE: "Campfire",
            ENTITY_TENT: "Tent",

            BUSH_LARGE: "Large Bush",
            BUSH_SMALL: "Small Bush",
        },
        "legends": {
            ITEM_LOG: "Good for fire or building.",
            ITEM_STICK: "A great crafting ingredient.",
            ITEM_AXE: "A tool, but also a weapon.",
            ITEM_TENT: "Temporary shelter for your journeys.",
            ITEM_MATCHES: "Something to start the fire with.",
            ITEM_CAMPFIRE: "Essential for your survival.",

            ROCK0: "A great crafting ingredient.",
            ROCK1: "A great crafting ingredient.",
            ROCK2: "My beloved.",
            ROCK3: "A great crafting ingredient.",
            ROCK4: "A great crafting ingredient.",

            ITEM_BERRIES0: "A light source of food.",
            ITEM_BLUEBERRIES: "A light source of food.",

            ITEM_PLANT0: "A great crafting ingredient.",
            ITEM_PLANT1: "A great crafting ingredient.",
            ITEM_PLANT2: "A great crafting ingredient.",
            ITEM_PLANT3: "A great crafting ingredient.",
        },
        "menu": {
            "main": {
                "title": "CAMPING",
                "buttons": [
                    "C - Continue",
                    "N - New Game",
                    "S - Settings",
                    "Q - Quit    "
                ]
            },
            "settings": {
                "lang_changed": "Changed language to {lang}.",
                "buttons": [
                    "L - Change Language  ",
                    "F - Toggle Fullscreen",
                    "S - Back to Main Menu"
                ]
            }
            
        },
        "actions": {
            "tired": "You are too tired to continue."
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

            ROCK0: "Kameň",
            ROCK1: "Kameň",
            ROCK2: "Kameň",
            ROCK3: "Kameň",
            ROCK4: "Kameň",

            ITEM_BERRIES0: "Bobule",
            ITEM_BLUEBERRIES: "Divoké Čučoriedky",

            ITEM_PLANT0: "Rastlina",
            ITEM_PLANT1: "Rastlina",
            ITEM_PLANT2: "Rastlina",
            ITEM_PLANT3: "Vysušená Rastlina",

            ENTITY_CAMPFIRE: "Táborák",
            ENTITY_TENT: "Stan",

            BUSH_LARGE: "Veľký Ker",
            BUSH_SMALL: "Malý Ker",
        },
        "legends": {
            ITEM_LOG: "Dobré na oheň alebo stavanie.",
            ITEM_STICK: "Skvelá prísada na tvorenie.",
            ITEM_AXE: "Nástroj, ale taktiež zbraň.",
            ITEM_TENT: "Dočasný prístrešok na tvoje cesty.",
            ITEM_MATCHES: "Hodia sa na založenie ohňa.",
            ITEM_CAMPFIRE: "Nevyhnutný na tvoje prežitie.",

            ROCK0: "Skvelá prísada na tvorenie.",
            ROCK1: "Skvelá prísada na tvorenie.",
            ROCK2: "Môj milovaný.",
            ROCK3: "Skvelá prísada na tvorenie.",
            ROCK4: "Skvelá prísada na tvorenie.",

            ITEM_BERRIES0: "Ľahký zdroj potravy.",
            ITEM_BLUEBERRIES: "Ľahký zdroj potravy.",

            ITEM_PLANT0: "Skvelá prísada na tvorenie.",
            ITEM_PLANT1: "Skvelá prísada na tvorenie.",
            ITEM_PLANT2: "Skvelá prísada na tvorenie.",
            ITEM_PLANT3: "Skvelá prísada na tvorenie.",
        },
        "menu": {
            "main": {
                "title": "KEMPOVAČKA",
                "buttons": [
                    "C - Pokračovať ",
                    "N - Nová Hra   ",
                    "S - Nastavenia ",
                    "Q - Opustiť Hru"
                ]
            },
            "settings": {
                "lang_changed": "Jazyk zmenený na {lang}.",
                "buttons": [
                    "L - Zmeniť Jazyk                 ",
                    "F - Prepnúť Režim Celej Obrazovky",
                    "S - Späť na Hlavné Menu          "
                ]
            }
            
        },
        "actions": {
            "tired": "Si príliš vyčerpaný aby si pokračoval."
        }
    }
}
# -------------


# --- Functions ---

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