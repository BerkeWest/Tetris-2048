import random
from tile_color import tile_colors

import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it


# Class used for modeling numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a tile with 2 as the number on it
    def __init__(self):
        self.foreground_color = None
        self.background_color = None
        random_numbers = [2, 4]
        # set the number on the tile
        self.number = random_numbers[random.randint(0, len(random_numbers) - 1)]
        # set the boundary color of the tile
        self.box_color = Color(132, 122, 113)  # box (boundary) color
        self.update_color()

    def update_color(self):
        self.background_color = tile_colors[self.number]['background_color']
        self.foreground_color = tile_colors[self.number]['foreground_color']

    # Method for drawing the tile
    def draw(self, position, length=1):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))
