from tile import Tile  # used for modeling each tile on the tetromino
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # module for generating random values/permutations
import numpy as np  # the fundamental Python module for scientific computing


# Class for modeling a tetromino (a 4-cell block used in the game of Tetris)
# The Tetromino class is used to create and manipulate tetrominoes in the game
# The class contains methods for moving, rotating, and drawing tetrominoes
# The class also contains methods for checking if a tetromino can be moved or rotated
class Tetromino:
    # The dimensions of the game grid
    grid_height, grid_width = None, None

    # Constructor for creating a tetromino with a given type (shape)
    # The type parameter is used to determine the shape of the tetromino
    # The occupied_tiles list is used to store the occupied (non-empty) tiles
    # in the tile matrix based on the type of the tetromino
    # The tile_matrix is a 2D matrix of numbered tiles based on the shape of the
    # 7 type of tetrominoes (I, O, Z, S, J, L, T) in their initial orientation
    def __init__(self, type):
        # set the shape of the tetromino based on the given type
        self.type = type
        # determine the occupied (non-empty) tiles in the tile matrix
        occupied_tiles = []
        if type == 'I':
            n = 4  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial orientation
            occupied_tiles.append((1, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((1, 3))
        elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial orientation
            occupied_tiles.append((0, 0))  # (column_index, row_index)
            occupied_tiles.append((1, 0))
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
        elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 1))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((2, 2))
        elif type == 'S':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 2))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((2, 1))
        elif type == 'J':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((2, 0))  # (column_index, row_index)
            occupied_tiles.append((2, 1))
            occupied_tiles.append((2, 2))
            occupied_tiles.append((1, 2))
        elif type == 'L':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 0))  # (column_index, row_index)
            occupied_tiles.append((0, 1))
            occupied_tiles.append((0, 2))
            occupied_tiles.append((1, 2))
        elif type == 'T':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 1))  # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
            occupied_tiles.append((1, 2))
        # create a matrix of numbered tiles based on the shape of the tetromino
        self.tile_matrix = np.full((n, n), None)
        # create the four tiles (minos) of the tetromino and place these tiles
        # into the tile matrix
        for i in range(len(occupied_tiles)):
            col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
            # create the tile at the computed position
            self.tile_matrix[row_index][col_index] = Tile()
        # initialize the position of the tetromino (the bottom left cell in the
        # tile matrix) with a random horizontal position above the game grid
        self.bottom_left_cell = Point()
        self.bottom_left_cell.y = self.grid_height - 1
        self.bottom_left_cell.x = random.randint(0, self.grid_width - n)

    # Method that returns the position of the cell in the tile matrix specified
    # by the given row and column indexes
    # The rotated parameter is used to determine the position of the cell in the
    # tile matrix after a 90-degree rotation
    def get_cell_position(self, row, col, rotated=False):
        n = len(self.tile_matrix)
        if rotated:
            return Point(self.bottom_left_cell.x + (n - 1 - col), self.bottom_left_cell.y + row)
        else:
            return Point(self.bottom_left_cell.x + col, self.bottom_left_cell.y + (n - 1 - row))

    # Method that returns a copy of tile_matrix omitting empty rows and columns
    # and the position of the bottom left cell when return_position is set
    def get_min_bounded_tile_matrix(self, return_position=False):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        # determine rows and columns to copy (omit empty rows and columns)
        min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
        for row in range(n):
            for col in range(n):
                if self.tile_matrix[row][col] is not None:
                    if row < min_row:
                        min_row = row
                    if row > max_row:
                        max_row = row
                    if col < min_col:
                        min_col = col
                    if col > max_col:
                        max_col = col
        # copy the tiles from the tile matrix and return the resulting copy
        copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if self.tile_matrix[row][col] is not None:
                    row_ind = row - min_row
                    col_ind = col - min_col
                    copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
        # return just the resulting copy matrix when return_position is not set
        if not return_position:
            return copy
        # otherwise return the position of the bottom left cell in copy as well
        else:
            blc_position = cp.copy(self.bottom_left_cell)
            blc_position.translate(min_col, (n - 1) - max_row)
            return copy, blc_position

    # Method for drawing the tetromino on the game grid
    def draw(self):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
                # draw each occupied tile (not equal to None) on the game grid
                if self.tile_matrix[row][col] is not None:
                    # get the position of the tile
                    position = self.get_cell_position(row, col)
                    # draw only the tiles that are inside the game grid
                    if position.y < self.grid_height:
                        self.tile_matrix[row][col].draw(position)

                        # Method for moving the tetromino in a given direction by 1 on the game grid

    # The direction parameter is used to determine the direction of the movement
    # The game_grid parameter is used to check if the tetromino can be moved in
    # the given direction or not by using the can_be_moved method defined below
    def move(self, direction, game_grid):
        # check if the tetromino can be moved in the given direction by using the
        # can_be_moved method defined below
        if not (self.can_be_moved(direction, game_grid)):
            return False  # the tetromino cannot be moved in the given direction
        # move the tetromino by updating the position of the bottom left cell in
        # the tile matrix
        if direction == "left":
            self.bottom_left_cell.x -= 1
        elif direction == "right":
            self.bottom_left_cell.x += 1
        else:  # direction == "down"
            self.bottom_left_cell.y -= 1
        return True  # successful move in the given direction

    # Method to check if the tetromino can be moved in the given direction or not
    def can_be_moved(self, dir, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        # check for moving left or right
        if dir == "left" or dir == "right":
            for row in range(n):
                for col in range(n):
                    # direction = left --> check the leftmost tile of each row
                    if dir == "left" and self.tile_matrix[row][col] is not None:
                        leftmost = self.get_cell_position(row, col)
                        # tetromino cannot go left if any leftmost tile is at x = 0
                        if leftmost.x == 0:
                            return False
                        # skip each row whose leftmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if leftmost.y >= self.grid_height:
                            break
                        # the tetromino cannot go left if the grid cell on the left of
                        # any leftmost tile is occupied
                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False
                        break  # end the inner for loop
                    # direction = right --> check the rightmost tile of each row
                    elif dir == "right" and self.tile_matrix[row][n - 1 - col] is not None:
                        rightmost = self.get_cell_position(row, n - 1 - col)
                        # the tetromino cannot go right if any rightmost tile is at
                        # x = grid_width - 1
                        if rightmost.x == self.grid_width - 1:
                            return False
                        # skip each row whose rightmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if rightmost.y >= self.grid_height:
                            break
                        # the tetromino cannot go right if the grid cell on the right
                        # of any rightmost tile is occupied
                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False
                        break  # end the inner for loop
        # direction = down --> check the bottommost tile of each column
        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    if self.tile_matrix[row][col] is not None:
                        bottommost = self.get_cell_position(row, col)
                        # skip each column whose bottommost tile is out of the grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if bottommost.y > self.grid_height:
                            break
                        # tetromino cannot go down if any bottommost tile is at y = 0
                        if bottommost.y == 0:
                            return False
                            # or the grid cell below any bottommost tile is occupied
                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False
                        break  # end the inner for loop
        return True  # tetromino can be moved in the given direction

    # Method for rotating the tetromino in a given direction by 90 degrees
    # The direction parameter is used to determine the direction of the rotation
    # The can_rotate method defined below is used to check if the tetromino can
    # be rotated in the given direction or not
    def rotate(self, direction):
        if not (self.can_rotate(direction)):
            return False
        if direction == "d":
            self.tile_matrix = np.rot90(self.tile_matrix, 3)
        elif direction == "a":
            self.tile_matrix = np.rot90(self.tile_matrix, 1)
        return True

    # Method to check if the tetromino can be rotated in the given direction or not
    # The dir parameter is used to determine the direction of the rotation
    # The can_rotate method returns True if the tetromino can be rotated in the
    # given direction and False otherwise
    def can_rotate(self, dir):
        n = len(self.tile_matrix)
        copy_of_tile_matrix = cp.copy(self.tile_matrix)

        for row in range(n):
            for col in range(n):
                if dir == "d" and copy_of_tile_matrix[row][col] is not None:
                    copy_of_tile_matrix = np.rot90(copy_of_tile_matrix, 3)
                    position = self.get_cell_position(row, col)
                    if position.y < 0 or position.x < 0 or position.x >= self.grid_width:
                        return False

                elif dir == "a" and copy_of_tile_matrix[row][col] is not None:
                    copy_of_tile_matrix = np.rot90(copy_of_tile_matrix, 1)
                    position = self.get_cell_position(row, col)
                    if position.y < 0 or position.x < 0 or position.x >= self.grid_width:
                        return False
        return True
