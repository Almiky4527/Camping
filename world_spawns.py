from utils.identifiers import *


INITIAL_GENERATION = [
    {
        "grid": (38, 22),
        "spawns": [
            {
                "weight": 2
            },
            {
                "id": PINE_SMALL,
                "weight": 1,
                "scatter": (25, 15)
            },
            {
                "id": PINE_LARGE,
                "weight": 1,
                "scatter": (25, 15)
            },
            {
                "id": OAK_SMALL,
                "weight": 1,
                "scatter": (25, 15)
            },
            {
                "id": OAK_LARGE,
                "weight": 1,
                "scatter": (25, 15)
            }
        ]
    },
    {
        "grid": (31, 17),
        "spawns": [
            {
                "weight": 40
            },
            {
                "id": ROCK0,
                "weight": 2,
                "scatter": (50, 30)
            },
            {
                "id": ROCK1,
                "weight": 2,
                "scatter": (50, 30)
            },
            {
                "id": ROCK2,
                "weight": 1,
                "scatter": (50, 30)
            },
            {
                "id": ROCK3,
                "weight": 2,
                "scatter": (50, 30)
            },
            {
                "id": ROCK4,
                "weight": 2,
                "scatter": (50, 30)
            }
        ]
    },
    {
        "grid": (40, 25),
        "spawns": [
            {
                "weight": 20
            },
            {
                "id": BUSH_LARGE,
                "weight": 1,
                "scatter": (50, 30)
            },
            {
                "id": BUSH_SMALL,
                "weight": 1,
                "scatter": (50, 30)
            }
        ]
    },
    {
        "grid": (35, 20),
        "spawns": [
            {
                "weight": 50
            },
            {
                "id": PLANT0,
                "weight": 3,
                "scatter": (50, 30),
                "scattered_positions": (1, 4)
            },
            {
                "id": PLANT1,
                "weight": 3,
                "scatter": (50, 30),
                "scattered_positions": (1, 4)
            },
            {
                "id": PLANT2,
                "weight": 1,
                "scatter": (50, 30),
                "scattered_positions": (1, 3)
            },
            {
                "id": PLANT3,
                "weight": 1,
                "scatter": (50, 30),
                "scattered_positions": (1, 2)
            }
        ]
    }
]


RANDOM_SPAWNS = {
    SEASON_SPRING: [
        {
            "grid": (35, 20),
            "spawns": [
                {
                    "weight": 120
                },
                {
                    "id": PLANT0,
                    "weight": 3,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 3)
                },
                {
                    "id": PLANT1,
                    "weight": 3,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 3)
                },
                {
                    "id": PLANT2,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                },
                {
                    "id": PLANT3,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                }
            ]
        }
    ],
    SEASON_SUMMER: [
        {
            "grid": (35, 20),
            "spawns": [
                {
                    "weight": 100
                },
                {
                    "id": PLANT0,
                    "weight": 5,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 3)
                },
                {
                    "id": PLANT1,
                    "weight": 5,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 3)
                },
                {
                    "id": PLANT2,
                    "weight": 3,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                },
                {
                    "id": PLANT3,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                }
            ]
        }
    ],
    SEASON_AUTUMN: [
        {
            "grid": (35, 20),
            "spawns": [
                {
                    "weight": 150
                },
                {
                    "id": PLANT0,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                },
                {
                    "id": PLANT1,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                },
                {
                    "id": PLANT2,
                    "weight": 1,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 2)
                },
                {
                    "id": PLANT3,
                    "weight": 3,
                    "scatter": (50, 30),
                    "scattered_positions": (1, 3)
                }
            ]
        }
    ],
    SEASON_WINTER: [
        {
            "grid": (35, 20),
            "spawns": []
        }
    ]
}


RANDOM_ANIMAL_SPAWNS = {
    SEASON_SPRING: [
        {
            "id": ANIMAL_HARE,
            "count": (3, 6),
            "dtp": 700
        }
    ],
    SEASON_SUMMER: [
        {
            "id": ANIMAL_HARE,
            "count": (3, 4),
            "dtp": 700
        },
        {
            "id": ANIMAL_DEER,
            "count": (0, 2),
            "dtp": 1000
        }
    ],
    SEASON_AUTUMN: [
        {
            "id": ANIMAL_HARE,
            "count": (0, 3),
            "chance": 0.1,
            "dtp": 700
        },
        {
            "id": ANIMAL_DEER,
            "count": (0, 1),
            "chance": 0.1,
            "dtp": 1000
        }
    ],
    SEASON_WINTER: [
        {
            "id": ANIMAL_BEAR,
            "count": (0, 1),
            "chance": 0.01,
            "dtp": 1300
        }
    ]
}


RANDOM_DESPAWNS = {
    "plant": 0.2,
    "item_plant": 0.5,
    "food": 0.4,
    "meat": 0.4
}