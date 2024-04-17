from lib.color import Color

# Dictionary containing the colors for the tiles based on the number on them
# The dictionary is used in the Tile class in the update_color method
# The dictionary is used to set the background and foreground colors of the tile
tile_colors = {
    2: {
        "background_color": Color(238, 228, 218),
        "foreground_color": Color(138, 129, 120)
    },
    4: {
        "background_color": Color(237, 224, 200),
        "foreground_color": Color(138, 129, 120)
    },
    8: {
        "background_color": Color(242, 177, 121),
        "foreground_color": Color(255, 255, 255)
    },
    16: {
        "background_color": Color(245, 149, 99),
        "foreground_color": Color(255, 255, 255)
    },
    32: {
        "background_color": Color(246, 124, 95),
        "foreground_color": Color(255, 255, 255)
    },
    64: {
        "background_color": Color(246, 94, 59),
        "foreground_color": Color(255, 255, 255)
    },
    128: {
        "background_color": Color(237, 207, 114),
        "foreground_color": Color(255, 255, 255)
    },
    256: {
        "background_color": Color(237, 204, 97),
        "foreground_color": Color(255, 255, 255)
    },
    512: {
        "background_color": Color(237, 200, 80),
        "foreground_color": Color(255, 255, 255)
    },
    1024: {
        "background_color": Color(237, 197, 63),
        "foreground_color": Color(255, 255, 255)
    },
    2048: {
        "background_color": Color(237, 197, 46),
        "foreground_color": Color(255, 255, 255)
    }
}
