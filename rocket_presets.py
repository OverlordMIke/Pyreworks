import random

ROCKET_PRESETS = {
    "ClassicRandom": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": [
                {
                    "particle_count": 110,
                    "count_randomness": 30,
                    "colour": ("random","random","random"),
                    "explosive_force_min": 0.5,
                    "explosive_force_max": 40,
                    "life": 1.0,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                }
            ]
        },
        "fuel": 1,
        "thrust_strength": 180,
        "fuse": 3,
    },
    "Flower": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": [
                {
                    "particle_count": 110,
                    "count_randomness": 30,
                    "colour": ("random","random","random"),
                    "explosive_force_min": 0.5,
                    "explosive_force_max": 40,
                    "life": 4,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                },
                {
                    "particle_count": 60,
                    "count_randomness": 30,
                    "colour": (255, 178, 0),
                    "explosive_force_min": 0.5,
                    "explosive_force_max": 10,
                    "life": 4,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                }
            ]
        },
        "fuel": 1,
        "thrust_strength": 180,
        "fuse": 3,
    },
    "TwoTime": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": [
                {
                    "particle_count": 110,
                    "count_randomness": 30,
                    "colour": ("random","random","random"),
                    "explosive_force_min": 0.5,
                    "explosive_force_max": 40,
                    "life": 4,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                },
                {
                    "particle_count": 110,
                    "count_randomness": 30,
                    "colour": ("random","random","random"),
                    "explosive_force_min": 35,
                    "explosive_force_max": 80,
                    "life": 4,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                }
            ]
        },
        "fuel": 1,
        "thrust_strength": 180,
        "fuse": 3,
    },
    "Patriot": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": [
                {
                    "particle_count": 200,
                    "count_randomness": 30,
                    "colour": (255,255,255),
                    "explosive_force_min": 0.5,
                    "explosive_force_max": 60,
                    "life": 3.5,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                },
                {
                    "particle_count": 90,
                    "count_randomness": 30,
                    "colour": (10,10,255),
                    "explosive_force_min": 5,
                    "explosive_force_max": 40,
                    "life": 3,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                },
                {
                    "particle_count": 300,
                    "count_randomness": 30,
                    "colour": (255,10,10),
                    "explosive_force_min": 35,
                    "explosive_force_max": 60,
                    "life": 3,
                    "decay": 0.75,
                    "decay_randomness": 0.25
                }
            ]
        },
        "fuel": 3,
        "thrust_strength": 90,
        "fuse": 4.5,
    },
}