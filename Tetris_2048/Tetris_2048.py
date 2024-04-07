import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
GRID_HEIGHT = 16
GRID_WIDTH = 16
INFO_WIDTH = 8
BACKGROUND_COLOR = Color(139, 120, 128)
BUTTON_COLOR = Color(100, 100, 128)
TEXT_COLOR = Color(31, 160, 239)
BLACK_COLOR = Color(0, 0, 0)
WHITE_COLOR = Color(255, 255, 255)
MENU_IMAGE_PATH = "/images/menu_image.png"
BUTTON_TEXT = "Click Here to Go Settings Screen"
SLIDER_X = 280
SLIDER_Y_WIDTH = 455
SLIDER_Y_HEIGHT = 405
SLIDER_RADIUS = 10
CONTINUE_BUTTON_CENTER = [250, 100]
CONTINUE_BUTTON_WIDTH = 300
CONTINUE_BUTTON_HEIGHT = 50
SLIDER_MIN_X = 130
SLIDER_MAX_X = 430
WIDTH_MIN_VALUE = 12
WIDTH_MAX_VALUE = 24
HEIGHT_MIN_VALUE = 12
HEIGHT_MAX_VALUE = 24
SLIDER_BAR_Y_WIDTH = 450
SLIDER_BAR_Y_HEIGHT = 400
SLIDER_BAR_WIDTH = 300
SLIDER_BAR_HEIGHT = 10


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------


def start():
    stddraw.setCanvasSize(CANVAS_WIDTH, CANVAS_HEIGHT)
    stddraw.setXscale(-0.5, GRID_WIDTH)
    stddraw.setYscale(-0.5, GRID_HEIGHT)
    display_game_menu(GRID_WIDTH, GRID_HEIGHT + 0.5)
    grid_h, grid_w = settings_screen()
    game_w = grid_w + INFO_WIDTH
    stddraw.setXscale(-0.5, game_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w, INFO_WIDTH)
    current_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino

    while True:
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed in ["left", "right", "down"]:
                current_tetromino.move(key_typed, grid)
            elif key_typed in ["d", "a"]:
                current_tetromino.rotate(key_typed)
            elif key_typed == "space":
                while current_tetromino.can_be_moved("down", grid):
                    current_tetromino.move("down", grid)
            stddraw.clearKeysTyped()

        success = current_tetromino.move("down", grid)
        if not success:
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            game_over = grid.update_grid(tiles, pos)
            if game_over:
                break
            current_tetromino = create_tetromino(grid_h, grid_w)
            grid.current_tetromino = current_tetromino

        grid.display()

    print("Game over")


# Function for creating random shaped tetrominoes
def create_tetromino(grid_height, grid_width):
    tetromino_types = ['I', 'O', 'Z', 'S', 'J', 'L', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    return Tetromino(random_type)


def settings_screen():
    stddraw.setXscale(0, 500)
    stddraw.setYscale(0, 500)
    sliderPositions = [SLIDER_X, SLIDER_X]
    gridSizeValues = [18, 18]  # Default grid size values

    while True:
        stddraw.clear(BACKGROUND_COLOR)
        # Draw slider bars for width and height
        stddraw.setPenColor(BLACK_COLOR)
        stddraw.filledRectangle(SLIDER_X - SLIDER_BAR_WIDTH / 2, SLIDER_BAR_Y_WIDTH, SLIDER_BAR_WIDTH,
                                SLIDER_BAR_HEIGHT)
        stddraw.filledRectangle(SLIDER_X - SLIDER_BAR_WIDTH / 2, SLIDER_BAR_Y_HEIGHT, SLIDER_BAR_WIDTH,
                                SLIDER_BAR_HEIGHT)
        # Draw slider outlines
        stddraw.setPenColor(BUTTON_COLOR)
        stddraw.rectangle(SLIDER_X - SLIDER_BAR_WIDTH / 2, SLIDER_BAR_Y_WIDTH, SLIDER_BAR_WIDTH + 0.5,
                          SLIDER_BAR_HEIGHT + 0.5)
        stddraw.rectangle(SLIDER_X - SLIDER_BAR_WIDTH / 2, SLIDER_BAR_Y_HEIGHT, SLIDER_BAR_WIDTH + 0.5,
                          SLIDER_BAR_HEIGHT + 0.5)
        # Draw slider knobs
        stddraw.setPenColor(WHITE_COLOR)
        stddraw.filledCircle(sliderPositions[0], SLIDER_Y_WIDTH, SLIDER_RADIUS)
        stddraw.filledCircle(sliderPositions[1], SLIDER_Y_HEIGHT, SLIDER_RADIUS)
        # Draw slider values
        stddraw.setPenColor(BLACK_COLOR)
        stddraw.text(sliderPositions[0], SLIDER_Y_WIDTH, str(int(gridSizeValues[0])))
        stddraw.text(sliderPositions[1], SLIDER_Y_HEIGHT, str(int(gridSizeValues[1])))
        stddraw.setFontSize(14)
        stddraw.boldText(100, SLIDER_Y_WIDTH + 2, "Width:")
        stddraw.boldText(100, SLIDER_Y_HEIGHT + 2, "Height:")
        # Draw continue button
        stddraw.setPenColor(BUTTON_COLOR)
        stddraw.filledRectangle(CONTINUE_BUTTON_CENTER[0] - CONTINUE_BUTTON_WIDTH / 2,
                                CONTINUE_BUTTON_CENTER[1] - CONTINUE_BUTTON_HEIGHT / 2,
                                CONTINUE_BUTTON_WIDTH, CONTINUE_BUTTON_HEIGHT)
        stddraw.setPenColor(BLACK_COLOR)
        stddraw.text(CONTINUE_BUTTON_CENTER[0], CONTINUE_BUTTON_CENTER[1], "Start!")

        stddraw.show(10)

        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # Adjust width slider
            if SLIDER_BAR_Y_WIDTH - SLIDER_RADIUS <= mouse_y <= SLIDER_BAR_Y_WIDTH + SLIDER_RADIUS:
                if SLIDER_X - SLIDER_BAR_WIDTH / 2 <= mouse_x <= SLIDER_X + SLIDER_BAR_WIDTH / 2:
                    sliderPositions[0] = mouse_x
                    gridSizeValues[0] = p_to_c(mouse_x, SLIDER_MIN_X, SLIDER_MAX_X, WIDTH_MIN_VALUE,
                                               WIDTH_MAX_VALUE)
            # Adjust height slider
            elif SLIDER_BAR_Y_HEIGHT - SLIDER_RADIUS <= mouse_y <= SLIDER_BAR_Y_HEIGHT + SLIDER_RADIUS:
                if SLIDER_X - SLIDER_BAR_WIDTH / 2 <= mouse_x <= SLIDER_X + SLIDER_BAR_WIDTH / 2:
                    sliderPositions[1] = mouse_x
                    gridSizeValues[1] = p_to_c(mouse_x, SLIDER_MIN_X, SLIDER_MAX_X, HEIGHT_MIN_VALUE,
                                               HEIGHT_MAX_VALUE)
            # Check continue button click
            if CONTINUE_BUTTON_CENTER[0] - CONTINUE_BUTTON_WIDTH / 2 <= mouse_x <= CONTINUE_BUTTON_CENTER[
                0] + CONTINUE_BUTTON_WIDTH / 2 and \
                    CONTINUE_BUTTON_CENTER[1] - CONTINUE_BUTTON_HEIGHT / 2 <= mouse_y <= CONTINUE_BUTTON_CENTER[
                1] + CONTINUE_BUTTON_HEIGHT / 2:
                break

    return gridSizeValues[1], gridSizeValues[0]


def p_to_c(x, in_min, in_max, out_min, out_max):
    return int(round(((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)))


def display_game_menu(grid_height, grid_width):
    stddraw.clear(BACKGROUND_COLOR)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + MENU_IMAGE_PATH
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 6.5
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    button_w, button_h = grid_width - 1.5, 2
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5
    stddraw.setPenColor(BUTTON_COLOR)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(TEXT_COLOR)
    stddraw.text(img_center_x, button_blc_y + 1, BUTTON_TEXT)
    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w and button_blc_y <= mouse_y <= button_blc_y + button_h:
                break


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
# Main function where this program starts execution
