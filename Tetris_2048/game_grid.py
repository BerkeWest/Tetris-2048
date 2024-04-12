import sys
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from tile import Tile
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w, info_w, game_speed):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.info_width = info_w
        self.game_speed = game_speed
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        self.next_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(139, 120, 128)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 0, 0)
        self.boundary_color = Color(0, 0, 0)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.001
        self.box_thickness = 3 * self.line_thickness
        self.score = 0

    # Method used for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.score = Tile.merge_tiles(self.tile_matrix, self.score)
        self.draw_boundaries()
        self.draw_info_panel()

        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(self.game_speed)

    # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    def draw_info_panel(self):
        stddraw.setPenColor(Color(139, 120, 128))
        stddraw.filledRectangle(self.grid_width - 0.5, -0.5, self.info_width, self.grid_height + 0.5)
        info_center_x_scale = self.grid_width + self.info_width / 2 - 0.5
        info_score_y_scale = self.grid_height - 2

        # Draw the score
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, info_score_y_scale, "Your Score: " + str(self.score))

        # Draw the "esc" to stop
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 3, "ESC=Stop")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 4, "A-D=Rotate")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 6, "Left-Right Arrow=Move")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 5, "Space=Hard Drop")
        stddraw.boldText(info_center_x_scale, info_score_y_scale - 7, "Down Arrow=Soft Drop")

        # Exit game button positioning
        button_height = 1
        button_width = self.info_width - 2
        button_top = 0.5  # Distance from bottom of the info panel
        button_center_y = button_top + button_height / 2

        stddraw.setPenColor(self.boundary_color)
        stddraw.filledRectangle(self.grid_width + 0.5, button_top, button_width, button_height)
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(20)
        stddraw.boldText(info_center_x_scale, button_center_y, "Exit Game")

        # Handle button click
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if (self.grid_width + 0.5 <= mouse_x <= self.grid_width + button_width + 0.5 and
                    button_top <= mouse_y <= button_top + button_height):
                sys.exit()  # Exit the program if the button is clicked

        # Method used for checking whether the grid cell with given row and column
        # indexes is occupied by a tile or empty

    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None

        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos_x = blc_position.x + col
                    pos_y = blc_position.y + (n_rows - 1) - row
                    # check if the position is inside the game grid
                    if self.is_inside(pos_y, pos_x):
                        self.tile_matrix[pos_y][pos_x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
                        return self.game_over

        # After locking the tiles, remove the full rows and update the grid
        self.remove_full_rows_and_shift()

        return self.game_over

    def remove_full_rows_and_shift(self):
        for row in range(self.grid_height):
            if None not in self.tile_matrix[row]:
                self.score += sum(tile.number for tile in self.tile_matrix[row] if tile is not None)
                for shift_row in range(row, self.grid_height - 1):
                    self.tile_matrix[shift_row] = self.tile_matrix[shift_row + 1]
                self.tile_matrix[self.grid_height - 1] = [None] * self.grid_width
