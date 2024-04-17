import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes


# Configuration classes
class Colors:
    BACKGROUND = Color(84, 73, 78)
    BUTTON = Color(90, 90, 90)
    TEXT = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)


class Texts:
    BUTTON_TEXT = "Press Here or Space to Go Settings"
    GAME_OVER_WIN = "Game Over, You Win"
    GAME_OVER_LOSE = "Game Over, You Lose"
    PLAY_AGAIN = "Play Again"
    START_GAME = "Press Here or Space to Start!"
    HOW_TO_PLAY = (
        "Use 'A' to rotate the tetromino counter-clockwise and 'D' to rotate it clockwise. "
        "Use the Left and Right Arrow Keys to move the tetromino sideways. Down arrow to soft drop "
        "and the space bar for a hard drop. You lose if a tetromino exits the play area, "
        "and you win the game if a tetromino score reaches 2048. You can also press 'ESC' to stop game. "
    )


class Dimensions:
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 800
    GRID_HEIGHT = 16
    GRID_WIDTH = 16
    INFO_WIDTH = 8
    SLIDER_RADIUS = 10
    SLIDER_X = 280
    SLIDER_Y_WIDTH = 455
    SLIDER_Y_HEIGHT = 405
    SLIDER_Y_SPEED = 375
    CONTINUE_BUTTON_CENTER = [250, 100]
    CONTINUE_BUTTON_WIDTH = 300
    CONTINUE_BUTTON_HEIGHT = 50
    SLIDER_MIN_X = 130
    SLIDER_MAX_X = 430
    SLIDER_MIN_XX = 130
    SLIDER_MAX_XX = 430
    WIDTH_MIN_VALUE = 12
    WIDTH_MAX_VALUE = 24
    HEIGHT_MIN_VALUE = 18
    HEIGHT_MAX_VALUE = 24
    SLIDER_BAR_Y_WIDTH = 450
    SLIDER_BAR_Y_HEIGHT = 400
    SLIDER_BAR_WIDTH = 300
    SLIDER_BAR_HEIGHT = 10
    SLIDER_BAR_Y_SPEED = 350
    SPEED_MAX_VALUE = 500
    SPEED_MIN_VALUE = 50
    MENU_IMAGE_PATH = "/images/menu_image.png"
    GAME_OVER_LOSE_PATH = "/images/loseMenu_image.png"
    GAME_OVER_WIN_PATH = "/images/winMenu_image.png"
    GAME_PAUSED_PATH = "/images/pauseMenu_image.png"


# Main program function
def start():
    stddraw.setXscale(-0.5, Dimensions.GRID_WIDTH)
    stddraw.setYscale(-0.5, Dimensions.GRID_HEIGHT)
    display_game_menu(Dimensions.GRID_WIDTH, Dimensions.GRID_HEIGHT)
    grid_h, grid_w, game_speed = display_settings_screen()
    game_w = grid_w + Dimensions.INFO_WIDTH
    stddraw.setXscale(-0.5, game_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w, Dimensions.INFO_WIDTH, game_speed)
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino
    next_tetromino = create_tetromino()
    grid.next_tetromino = next_tetromino

    while True:
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "escape":
                display_pause_screen(grid.score)
            elif key_typed in ["left", "right", "down"]:
                current_tetromino.move(key_typed, grid)
            elif key_typed in ["d", "a"]:
                current_tetromino.rotate(key_typed)
            elif key_typed == "space":
                while current_tetromino.can_be_moved("down", grid):
                    current_tetromino.move("down", grid)
            elif key_typed == "r":
                start()
            stddraw.clearKeysTyped()

        success = current_tetromino.move("down", grid)
        if not success:
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            game_over = grid.update_grid(tiles, pos)
            if game_over:
                is_restarted = display_game_over_screen(grid_h, game_w, grid.score)
                if is_restarted:
                    grid = GameGrid(grid_h, grid_w, Dimensions.INFO_WIDTH, game_speed)
                elif not is_restarted:
                    start()
            current_tetromino = next_tetromino
            next_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = next_tetromino

        grid.display()


# Function for creating random shaped tetrominoes
def create_tetromino():
    tetromino_types = ['I', 'O', 'Z', 'S', 'J', 'L', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    return Tetromino(random_type)


def p_to_c(x, in_min, in_max, out_min, out_max):
    return int(round(((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)))


def display_settings_screen():
    stddraw.setXscale(0, 500)
    stddraw.setYscale(0, 500)
    sliderPositions = [Dimensions.SLIDER_X, Dimensions.SLIDER_X, Dimensions.SLIDER_X]
    gridSizeValues = [18, 21]  # Default grid size values
    game_speed = 250  # Default speed value

    while True:
        stddraw.clear(Colors.BACKGROUND)
        # Draw slider bars for width, height, and speed
        stddraw.setPenColor(Colors.BLACK)
        stddraw.filledRectangle(Dimensions.SLIDER_X - Dimensions.SLIDER_BAR_WIDTH / 2, Dimensions.SLIDER_BAR_Y_WIDTH,
                                Dimensions.SLIDER_BAR_WIDTH,
                                Dimensions.SLIDER_BAR_HEIGHT)
        stddraw.filledRectangle(Dimensions.SLIDER_X - Dimensions.SLIDER_BAR_WIDTH / 2, Dimensions.SLIDER_BAR_Y_HEIGHT,
                                Dimensions.SLIDER_BAR_WIDTH,
                                Dimensions.SLIDER_BAR_HEIGHT)
        stddraw.filledRectangle(Dimensions.SLIDER_X - Dimensions.SLIDER_BAR_WIDTH / 2, Dimensions.SLIDER_BAR_Y_SPEED,
                                Dimensions.SLIDER_BAR_WIDTH,
                                Dimensions.SLIDER_BAR_HEIGHT)

        # Draw slider knobs
        stddraw.setPenColor(Colors.WHITE)
        stddraw.filledCircle(sliderPositions[0], Dimensions.SLIDER_BAR_Y_WIDTH + 5, Dimensions.SLIDER_RADIUS)
        stddraw.filledCircle(sliderPositions[1], Dimensions.SLIDER_BAR_Y_HEIGHT + 5, Dimensions.SLIDER_RADIUS)
        stddraw.filledCircle(sliderPositions[2], Dimensions.SLIDER_BAR_Y_SPEED + 5,
                             Dimensions.SLIDER_RADIUS)

        # Draw slider values
        stddraw.setPenColor(Colors.WHITE)
        stddraw.text(sliderPositions[0], Dimensions.SLIDER_Y_WIDTH + 20, str(int(gridSizeValues[0])))
        stddraw.text(sliderPositions[1], Dimensions.SLIDER_Y_HEIGHT + 20, str(int(gridSizeValues[1])))
        stddraw.text(sliderPositions[2], Dimensions.SLIDER_Y_SPEED, f" {game_speed}")

        # Labels for sliders
        stddraw.setFontSize(25)
        stddraw.setFontFamily("Arial")
        stddraw.boldText(100, Dimensions.SLIDER_Y_WIDTH + 25, "Width:")
        stddraw.boldText(100, Dimensions.SLIDER_Y_HEIGHT + 25, "Height:")
        stddraw.boldText(100, 375, "Game Speed (ms):")

        # Draw continue button
        stddraw.setPenColor(Colors.BUTTON)
        stddraw.filledRectangle(Dimensions.CONTINUE_BUTTON_CENTER[0] - Dimensions.CONTINUE_BUTTON_WIDTH / 2,
                                Dimensions.CONTINUE_BUTTON_CENTER[1] - Dimensions.CONTINUE_BUTTON_HEIGHT / 2,
                                Dimensions.CONTINUE_BUTTON_WIDTH,
                                Dimensions.CONTINUE_BUTTON_HEIGHT)
        stddraw.setPenColor(Colors.TEXT)
        stddraw.text(Dimensions.CONTINUE_BUTTON_CENTER[0], Dimensions.CONTINUE_BUTTON_CENTER[1], Texts.START_GAME)

        stddraw.show(10)

        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if Dimensions.SLIDER_BAR_Y_WIDTH - Dimensions.SLIDER_RADIUS <= mouse_y <= Dimensions.SLIDER_BAR_Y_WIDTH + Dimensions.SLIDER_RADIUS:
                if Dimensions.SLIDER_MIN_X <= mouse_x <= Dimensions.SLIDER_MAX_X:
                    sliderPositions[0] = mouse_x
                    gridSizeValues[0] = p_to_c(mouse_x, Dimensions.SLIDER_MIN_X, Dimensions.SLIDER_MAX_X,
                                               Dimensions.WIDTH_MIN_VALUE, Dimensions.WIDTH_MAX_VALUE)
            elif Dimensions.SLIDER_BAR_Y_HEIGHT - Dimensions.SLIDER_RADIUS <= mouse_y <= Dimensions.SLIDER_BAR_Y_HEIGHT + Dimensions.SLIDER_RADIUS:
                if Dimensions.SLIDER_MIN_X <= mouse_x <= Dimensions.SLIDER_MAX_X:
                    sliderPositions[1] = mouse_x
                    gridSizeValues[1] = p_to_c(mouse_x, Dimensions.SLIDER_MIN_XX, Dimensions.SLIDER_MAX_XX,
                                               Dimensions.HEIGHT_MIN_VALUE, Dimensions.HEIGHT_MAX_VALUE)
            elif Dimensions.SLIDER_BAR_Y_SPEED - Dimensions.SLIDER_RADIUS <= mouse_y <= Dimensions.SLIDER_BAR_Y_SPEED + Dimensions.SLIDER_RADIUS:
                if Dimensions.SLIDER_MIN_X <= mouse_x <= Dimensions.SLIDER_MAX_X:
                    sliderPositions[2] = mouse_x
                    game_speed = p_to_c(mouse_x, Dimensions.SLIDER_MIN_X, Dimensions.SLIDER_MAX_X,
                                        Dimensions.SPEED_MIN_VALUE,
                                        Dimensions.SPEED_MAX_VALUE)

            if Dimensions.CONTINUE_BUTTON_CENTER[0] - Dimensions.CONTINUE_BUTTON_WIDTH / 2 <= mouse_x <= \
                    Dimensions.CONTINUE_BUTTON_CENTER[
                        0] + Dimensions.CONTINUE_BUTTON_WIDTH / 2 and \
                    Dimensions.CONTINUE_BUTTON_CENTER[1] - Dimensions.CONTINUE_BUTTON_HEIGHT / 2 <= mouse_y <= \
                    Dimensions.CONTINUE_BUTTON_CENTER[
                        1] + Dimensions.CONTINUE_BUTTON_HEIGHT / 2:
                break
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "space":
                break

    return gridSizeValues[1], gridSizeValues[0], game_speed


def display_game_over_screen(grid_h, grid_w, current_score):
    stddraw.clear(Colors.BACKGROUND)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    game_over_text = Texts.GAME_OVER_WIN if current_score >= 2048 else Texts.GAME_OVER_LOSE
    img_file = current_dir + Dimensions.GAME_OVER_WIN_PATH if current_score >= 2048 else current_dir + Dimensions.GAME_OVER_LOSE_PATH
    img_center_x, img_center_y = (grid_w - 1) / 2, grid_h -6
    image_to_display = Picture(img_file)
    button_w, button_h = grid_w - 6, 1.4
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5
    menu_button_y = button_blc_y + 2

    stddraw.picture(image_to_display, img_center_x, img_center_y)

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(40)
    stddraw.boldText(img_center_x, img_center_y - 4, game_over_text)

    stddraw.setFontSize(25)
    stddraw.text(img_center_x, img_center_y - 6, "Score: " + str(current_score))

    stddraw.setPenColor(Colors.BUTTON)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(Colors.TEXT)
    stddraw.text(img_center_x, button_blc_y + 0.7, Texts.PLAY_AGAIN)

    stddraw.setPenColor(Colors.BUTTON)
    stddraw.filledRectangle(button_blc_x, menu_button_y, button_w, button_h)
    stddraw.setPenColor(Colors.TEXT)
    stddraw.text(img_center_x, menu_button_y + 0.7, "Return to Main Menu")

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w:
                if button_blc_y <= mouse_y <= button_blc_y + button_h:
                    return True
                elif menu_button_y <= mouse_y <= menu_button_y + button_h:
                    return False


def display_game_menu(grid_height, grid_width):
    stddraw.clear(Colors.BACKGROUND)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + Dimensions.MENU_IMAGE_PATH
    img_center_x, img_center_y = (grid_width - 0.75) / 2, grid_height - 3
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    button_w, button_h = grid_width - 1.5, 1.8
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5

    stddraw.setPenColor(Colors.BUTTON)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(Colors.TEXT)
    stddraw.text(img_center_x, button_blc_y + 1, Texts.BUTTON_TEXT)

    instructions = Texts.HOW_TO_PLAY.split(". ")
    instructions_y_position = 9
    stddraw.setFontSize(20)
    stddraw.setPenColor(Colors.WHITE)

    # Draw each line of the instructions
    for i, line in enumerate(instructions):
        stddraw.text(img_center_x, instructions_y_position - i, line)

    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_blc_x <= mouse_x <= button_blc_x + button_w and button_blc_y <= mouse_y <= button_blc_y + button_h:
                break
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "space":
                stddraw.clearKeysTyped()
                break


def display_pause_screen(current_score):
    stddraw.clear(Colors.BACKGROUND)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + Dimensions.GAME_PAUSED_PATH
    img_center_x, img_center_y = (Dimensions.GRID_WIDTH + Dimensions.INFO_WIDTH) / 2, Dimensions.GRID_HEIGHT - 3
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(40)
    stddraw.text(img_center_x, img_center_y - 4, "Press 'ESC' to Resume Game")
    stddraw.text(img_center_x, img_center_y - 6, "Your Current Score: " + str(current_score))
    while True:
        stddraw.show(50)
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "escape":
                stddraw.clearKeysTyped()
                break


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    stddraw.setCanvasSize(Dimensions.CANVAS_WIDTH, Dimensions.CANVAS_HEIGHT)

    start()
# Main function where this program starts execution
