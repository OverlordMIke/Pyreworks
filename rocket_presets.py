import random

ROCKET_PRESETS = {
    "ClassicRandom": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": (
                "random",
                "random",
                "random"
            )
        },
        "fuel": 1,
        "thrust_strength": 180,
        "fuse": 2,
    },
    "ClassicRed": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": (
                255,
                0,
                0
            )
        },
        "fuel": 7,
        "thrust_strength": 9,
        "fuse": 15,
    },
    "ClassicGreen": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": (
                0,
                255,
                0
            )
        },
        "fuel": 7,
        "thrust_strength": 9,
        "fuse": 15,
    },
    "ClassicBlue": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": (
                0,
                0,
                255
            )
        },
        "fuel": 7,
        "thrust_strength": 9,
        "fuse": 15,
    },
    "ClassicWhite": {
        "theme": {
            "body": (255,255,255),
            "exhaust": (240, 201, 0),
            "pattern": (
                255,
                255,
                255
            )
        },
        "fuel": 7,
        "thrust_strength": 9,
        "fuse": 15,
    }
}