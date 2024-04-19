import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes

# Configuration dictionaries for using colors, texts, and dimensions in the game

colors = {
    'BACKGROUND': Color(84, 73, 78),
    'BUTTON': Color(90, 90, 90),
    'TEXT': Color(255, 255, 255),
    'BLACK': Color(0, 0, 0),
    'WHITE': Color(255, 255, 255),
}

texts = {
    'BUTTON_TEXT': "Press Here or Space to Go Settings",
    'GAME_OVER_WIN': "Game Over, You Win",
    'GAME_OVER_LOSE': "Game Over, You Lose",
    'PLAY_AGAIN': "Play Again",
    'START_GAME': "Press Here or Space to Start!",
    'HOW_TO_PLAY': (
        "Use 'A' to rotate the tetromino counter-clockwise and 'D' to rotate it clockwise. "
        "Use the Left and Right Arrow Keys to move the tetromino sideways. Down arrow to soft drop "
        "and the space bar for a hard drop. You lose if a tetromino exits the play area, "
        "and you win the game if a tetromino score reaches 2048. You can also press 'ESC' to stop game. "
    ),
}

dimensions = {
    'CANVAS_WIDTH': 800,
    'CANVAS_HEIGHT': 800,
    'GRID_HEIGHT': 16,
    'GRID_WIDTH': 16,
    'INFO_WIDTH': 8,
    'SLIDER_RADIUS': 10,
    'SLIDER_X': 280,
    'SLIDER_Y_WIDTH': 455,
    'SLIDER_Y_HEIGHT': 405,
    'SLIDER_Y_SPEED': 375,
    'CONTINUE_BUTTON_CENTER': [250, 100],
    'CONTINUE_BUTTON_WIDTH': 300,
    'CONTINUE_BUTTON_HEIGHT': 50,
    'SLIDER_MIN_X': 130,
    'SLIDER_MAX_X': 430,
    'SLIDER_MIN_XX': 130,
    'SLIDER_MAX_XX': 430,
    'WIDTH_MIN_VALUE': 12,
    'WIDTH_MAX_VALUE': 24,
    'HEIGHT_MIN_VALUE': 18,
    'HEIGHT_MAX_VALUE': 24,
    'SLIDER_BAR_Y_WIDTH': 450,
    'SLIDER_BAR_Y_HEIGHT': 400,
    'SLIDER_BAR_WIDTH': 300,
    'SLIDER_BAR_HEIGHT': 10,
    'SLIDER_BAR_Y_SPEED': 350,
    'SPEED_MAX_VALUE': 500,
    'SPEED_MIN_VALUE': 50,
    'MENU_IMAGE_PATH': "/images/menu_image.png",
    'GAME_OVER_LOSE_PATH': "/images/loseMenu_image.png",
    'GAME_OVER_WIN_PATH': "/images/winMenu_image.png",
    'GAME_PAUSED_PATH': "/images/pauseMenu_image.png",
    'CONTROLS_IMAGE_PATH': "/images/controls_image.png",
}


# Main program function for starting the game and handling user input
def start():
    file_path = os.path.join(os.path.dirname(__file__), "best_score.txt")
    max_score = read_max_score_from_file(file_path)
    stddraw.setXscale(-0.5, dimensions['GRID_WIDTH'])
    stddraw.setYscale(-0.5, dimensions['GRID_HEIGHT'])
    display_game_menu(dimensions['GRID_WIDTH'], dimensions['GRID_HEIGHT'], max_score)
    grid_h, grid_w, game_speed = display_settings_screen()
    game_w = grid_w + dimensions['INFO_WIDTH']
    stddraw.setXscale(-0.5, game_w - 0.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w, dimensions['INFO_WIDTH'], game_speed)
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino
    next_tetromino = create_tetromino()
    grid.next_tetromino = next_tetromino
    grid.max_score = max_score

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
                if grid.score > max_score:
                    max_score = grid.score
                    write_max_score_to_file(max_score, file_path)
                is_restarted = display_game_over_screen(grid_h, game_w, grid.score)
                if is_restarted:
                    grid = GameGrid(grid_h, grid_w, dimensions['INFO_WIDTH'], game_speed)
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


# Function for converting pixel values to coordinate values on the slider
def p_to_c(x, in_min, in_max, out_min, out_max):
    return int(round(((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)))


# Function for displaying the settings screen for the game. It allows the user to change the grid size and game speed
# The user can start the game by clicking on the button or pressing the 'space' key
def display_settings_screen():
    stddraw.setXscale(0, 500)
    stddraw.setYscale(0, 500)
    sliderPositions = [dimensions['SLIDER_X'], dimensions['SLIDER_X'], dimensions['SLIDER_X']]
    gridSizeValues = [18, 21]  # Default grid size values
    game_speed = 250  # Default speed value

    while True:
        stddraw.clear(colors['BACKGROUND'])
        # Draw slider bars for width, height, and speed
        stddraw.setPenColor(colors['BLACK'])
        stddraw.filledRectangle(dimensions['SLIDER_X'] - dimensions['SLIDER_BAR_WIDTH'] / 2,
                                dimensions['SLIDER_BAR_Y_WIDTH'],
                                dimensions['SLIDER_BAR_WIDTH'], dimensions['SLIDER_BAR_HEIGHT'])
        stddraw.filledRectangle(dimensions['SLIDER_X'] - dimensions['SLIDER_BAR_WIDTH'] / 2,
                                dimensions['SLIDER_BAR_Y_HEIGHT'],
                                dimensions['SLIDER_BAR_WIDTH'], dimensions['SLIDER_BAR_HEIGHT'])
        stddraw.filledRectangle(dimensions['SLIDER_X'] - dimensions['SLIDER_BAR_WIDTH'] / 2,
                                dimensions['SLIDER_BAR_Y_SPEED'],
                                dimensions['SLIDER_BAR_WIDTH'], dimensions['SLIDER_BAR_HEIGHT'])

        # Show picture
        current_dir = os.path.dirname(os.path.realpath(__file__))
        img_file = current_dir + dimensions['CONTROLS_IMAGE_PATH']
        img_center_x, img_center_y = 250, 225
        image_to_display = Picture(img_file)
        stddraw.picture(image_to_display, img_center_x, img_center_y)

        # Draw slider knobs
        stddraw.setPenColor(colors['WHITE'])
        stddraw.filledCircle(sliderPositions[0], dimensions['SLIDER_BAR_Y_WIDTH'] + 5, dimensions['SLIDER_RADIUS'])
        stddraw.filledCircle(sliderPositions[1], dimensions['SLIDER_BAR_Y_HEIGHT'] + 5, dimensions['SLIDER_RADIUS'])
        stddraw.filledCircle(sliderPositions[2], dimensions['SLIDER_BAR_Y_SPEED'] + 5, dimensions['SLIDER_RADIUS'])

        # Draw slider values
        stddraw.setPenColor(colors['WHITE'])
        stddraw.text(sliderPositions[0], dimensions['SLIDER_Y_WIDTH'] + 20, str(int(gridSizeValues[0])))
        stddraw.text(sliderPositions[1], dimensions['SLIDER_Y_HEIGHT'] + 20, str(int(gridSizeValues[1])))
        stddraw.text(sliderPositions[2], dimensions['SLIDER_Y_SPEED'], f" {game_speed}")

        # Labels for sliders
        stddraw.setFontSize(20)
        stddraw.setFontFamily("Arial")
        stddraw.boldText(65, dimensions['SLIDER_Y_WIDTH'], "Width")
        stddraw.boldText(65, dimensions['SLIDER_Y_HEIGHT'], "Height")
        stddraw.boldText(65, dimensions['SLIDER_Y_SPEED'] - 18, "Game Speed (ms)")

        # Draw continue button
        stddraw.setPenColor(colors['BUTTON'])
        stddraw.filledRectangle(dimensions['CONTINUE_BUTTON_CENTER'][0] - dimensions['CONTINUE_BUTTON_WIDTH'] / 2,
                                dimensions['CONTINUE_BUTTON_CENTER'][1] - dimensions['CONTINUE_BUTTON_HEIGHT'] - 5 / 2,
                                dimensions['CONTINUE_BUTTON_WIDTH'], dimensions['CONTINUE_BUTTON_HEIGHT'])
        stddraw.setPenColor(colors['TEXT'])
        stddraw.boldText(dimensions['CONTINUE_BUTTON_CENTER'][0], dimensions['CONTINUE_BUTTON_CENTER'][1] - 25,
                         texts['START_GAME'])

        stddraw.show(10)

        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # Check which slider is being interacted with
            # Take the mouse input and update the slider position and value
            # First one is for width, take the mouse_x, update the slider position and for the real width value
            # call to p_to_c function and update the gridSizeValues[0] with the returned value
            # Same for the height and speed sliders as well
            if dimensions['SLIDER_BAR_Y_WIDTH'] - dimensions['SLIDER_RADIUS'] <= mouse_y <= dimensions[
                'SLIDER_BAR_Y_WIDTH'] + dimensions['SLIDER_RADIUS']:
                if dimensions['SLIDER_MIN_X'] <= mouse_x <= dimensions['SLIDER_MAX_X']:
                    sliderPositions[0] = mouse_x
                    gridSizeValues[0] = int(p_to_c(mouse_x, dimensions['SLIDER_MIN_X'], dimensions['SLIDER_MAX_X'],
                                                   dimensions['WIDTH_MIN_VALUE'], dimensions['WIDTH_MAX_VALUE']))
            elif dimensions['SLIDER_BAR_Y_HEIGHT'] - dimensions['SLIDER_RADIUS'] <= mouse_y <= dimensions[
                'SLIDER_BAR_Y_HEIGHT'] + dimensions['SLIDER_RADIUS']:
                if dimensions['SLIDER_MIN_XX'] <= mouse_x <= dimensions['SLIDER_MAX_XX']:
                    sliderPositions[1] = mouse_x
                    gridSizeValues[1] = int(p_to_c(mouse_x, dimensions['SLIDER_MIN_XX'], dimensions['SLIDER_MAX_XX'],
                                                   dimensions['HEIGHT_MIN_VALUE'], dimensions['HEIGHT_MAX_VALUE']))
            elif dimensions['SLIDER_BAR_Y_SPEED'] - dimensions['SLIDER_RADIUS'] <= mouse_y <= dimensions[
                'SLIDER_BAR_Y_SPEED'] + dimensions['SLIDER_RADIUS']:
                if dimensions['SLIDER_MIN_X'] <= mouse_x <= dimensions['SLIDER_MAX_X']:
                    sliderPositions[2] = mouse_x
                    game_speed = int(p_to_c(mouse_x, dimensions['SLIDER_MIN_X'], dimensions['SLIDER_MAX_X'],
                                            dimensions['SPEED_MIN_VALUE'], dimensions['SPEED_MAX_VALUE']))

            if dimensions['CONTINUE_BUTTON_CENTER'][0] - dimensions['CONTINUE_BUTTON_WIDTH'] / 2 <= mouse_x <= \
                    dimensions['CONTINUE_BUTTON_CENTER'][0] + dimensions['CONTINUE_BUTTON_WIDTH'] / 2 and \
                    dimensions['CONTINUE_BUTTON_CENTER'][1] - dimensions['CONTINUE_BUTTON_HEIGHT'] - 5 / 2 <= mouse_y <= \
                    dimensions['CONTINUE_BUTTON_CENTER'][1] + dimensions['CONTINUE_BUTTON_HEIGHT'] - 5 / 2:
                break
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "space":
                break

    return gridSizeValues[1], gridSizeValues[0], game_speed


# Function for displaying the game over screen when the game ends (either win or lose with  a different message and image)
def display_game_over_screen(grid_h, grid_w, current_score):
    stddraw.clear(colors['BACKGROUND'])
    current_dir = os.path.dirname(os.path.realpath(__file__))
    game_over_text = texts['GAME_OVER_WIN'] if current_score >= 2048 else texts['GAME_OVER_LOSE']
    img_file = current_dir + dimensions['GAME_OVER_WIN_PATH'] if current_score >= 2048 else current_dir + dimensions[
        'GAME_OVER_LOSE_PATH']
    img_center_x, img_center_y = (grid_w - 1) / 2, grid_h - 6
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

    stddraw.setPenColor(colors['BUTTON'])
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(colors['TEXT'])
    stddraw.text(img_center_x, button_blc_y + 0.7, texts['PLAY_AGAIN'])

    stddraw.setPenColor(colors['BUTTON'])
    stddraw.filledRectangle(button_blc_x, menu_button_y, button_w, button_h)
    stddraw.setPenColor(colors['TEXT'])
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


# Function for displaying the game menu screen with instructions on how to play the game
# The user can start the game by clicking on the button or pressing the 'space' key
def display_game_menu(grid_height, grid_width, max_score):
    stddraw.clear(colors['BACKGROUND'])
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + dimensions['MENU_IMAGE_PATH']
    img_center_x, img_center_y = (grid_width - 0.75) / 2, grid_height - 3
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    button_w, button_h = grid_width - 1.5, 1.8
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 1.5

    stddraw.setPenColor(colors['BUTTON'])
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(colors['TEXT'])
    stddraw.text(img_center_x, button_blc_y + 1, texts['BUTTON_TEXT'])
    stddraw.text(img_center_x, button_blc_y - 1, "Best Score: " + str(max_score))

    instructions = texts['HOW_TO_PLAY'].split(". ")
    instructions_y_position = 9
    stddraw.setFontSize(20)
    stddraw.setPenColor(colors['WHITE'])

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


# Function for displaying the pause screen when the game is paused by the user pressing the 'ESC' key
# It displays the current score and a message to resume the game
# The user can also return to the main menu by clicking on the button
def display_pause_screen(current_score):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    img_file = current_dir + dimensions['GAME_PAUSED_PATH']
    img_center_x, img_center_y = (dimensions['GRID_WIDTH'] + dimensions['INFO_WIDTH']) / 2, dimensions[
        'GRID_HEIGHT'] - 3
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(40)
    stddraw.text(img_center_x, img_center_y - 4, "Press 'ESC' to Resume Game")
    stddraw.text(img_center_x, img_center_y - 6, "Your Current Score: " + str(current_score))
    stddraw.setPenColor(colors['BUTTON'])
    stddraw.filledRectangle(img_center_x - 6, 3, 12, 2)
    stddraw.setPenColor(colors['TEXT'])
    stddraw.setFontSize(25)
    stddraw.text(img_center_x, 4, "Return to Main Menu")

    while True:
        stddraw.show(50)
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "escape":
                stddraw.clearKeysTyped()
                break
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if img_center_x - 6 <= mouse_x <= img_center_x + 6 and 3 <= mouse_y <= 5:
                start()


# function to read the maximum score from the file
def read_max_score_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            max_score = int(file.read().strip())
            return max_score
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


# function to write the maximum score to the file
def write_max_score_to_file(max_score, file_path):
    with open(file_path, "w") as file:
        file.write(str(max_score))


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    stddraw.setCanvasSize(dimensions['CANVAS_WIDTH'], dimensions['CANVAS_HEIGHT'])

    start()
# Main function where this program starts execution
