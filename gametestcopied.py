"""
Sprite move between different rooms.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_rooms
"""

import arcade
import os
import math

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10
SCREEN_TITLE = "Sprite Rooms Example"

MOVEMENT_SPEED = 5


class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None

        # Initialize sapling list, add this needed attribute to any room
        self.sapling_list = arcade.SpriteList()

def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.sapling_list = arcade.SpriteList() # List for saplings

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up on the right side
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                     SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)
            
    wall_positions = [
        (1, 2), (1, 7), 
        (2, 2), (2, 4), (2, 5), (2, 7),
        (3, 2), (3, 3), (3, 4), (3, 7),
        (4, 6), (4, 7),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 6),
        (6, 4), (6, 6), (6, 7),
        (7, 1), (7, 3), (7, 4),
        (8, 3), (8, 7),
        (9, 2), (9, 3), (9, 4), (9, 5), (9, 7),
        (10, 5), (10, 7),
        (11, 2), (11, 4), (11, 5), (11, 7), (11, 8),
        (12, 2)         
    ]

    # Create the walls based on the positions
    for pos in wall_positions:
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        wall.left = pos[0] * SPRITE_SIZE
        wall.bottom = pos[1] * SPRITE_SIZE
        room.wall_list.append(wall)

    # Add the sapling
    mushroom = arcade.Sprite(":resources:images/tiles/mushroomRed.png", SPRITE_SCALING)
    mushroom.center_x = 7 * SPRITE_SIZE + 30
    mushroom.center_y = 3 * SPRITE_SIZE - 15
    room.sapling_list.append(mushroom)

    # Load the background image for this level.
    room.background = arcade.load_texture(":resources:images/backgrounds/"
                                          "abstract_1.jpg")

    return room

def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Simple small toolbar, with either watering can or axe.
        self.current_tool = "watering_can"  # Start with the watering can selected
        self.hotbar_icons = {
            "watering_can": ":resources:images/items/watering_can.png",
            "axe": ":resources:images/items/axe.png"
        }
        self.hotbar_textures = {
            "watering_can": arcade.load_texture(self.hotbar_icons["watering_can"]),
            "axe": arcade.load_texture(self.hotbar_icons["axe"])
        }

        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # If you have coins or monsters, then copy and modify the line
        # above for each list.

        # Draw the hotbar at the bottom center of the screen
        hotbar_x = SCREEN_WIDTH // 2
        hotbar_y = 50  # Position at the bottom of the screen

        for idx, tool in enumerate(self.hotbar_icons):
            icon_x = hotbar_x + (idx - 0.5) * 80  # Adjust positions for multiple items

            # Draw the icon
            arcade.draw_texture_rectangle(
                icon_x, hotbar_y,
                50, 50,
                self.hotbar_textures[tool]
            )

            # Highlight the selected tool
            if tool == self.current_tool:
                arcade.draw_rectangle_outline(icon_x, hotbar_y, 60, 60, arcade.color.YELLOW, 3)

        # Draw saplings
        self.rooms[self.current_room].sapling_list.draw()

        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Switch tool with key press
        if key == arcade.key.KEY_1:
            self.current_tool = "watering_can"
        elif key == arcade.key.KEY_2:
            self.current_tool = "axe"

        print(f"Selected tool: {self.current_tool}")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        # Check distance between player and all saplings
        saplings_hit = []
        for sapling in self.rooms[self.current_room].sapling_list:
            distance_to_player = math.sqrt((self.player_sprite.center_x - sapling.center_x) ** 2 + (self.player_sprite.center_y - sapling.center_y) ** 2)
            distance_to_click = math.sqrt((x - sapling.center_x) ** 2 + (y - sapling.center_y) ** 2)

            # Check if sapling is within interaction range of the player and click
            if distance_to_player < 80 and distance_to_click < 50:  # Adjust these values to tweak distance to sapling
                saplings_hit.append(sapling)

        if saplings_hit:
            print("Sapling interacted with!")
            for sapling in saplings_hit:
                if not hasattr(sapling, "state"):
                    sapling.state = "default"

                # Change sapling state based on interaction
                if sapling.state == "default":
                    sapling.state = "watered"
                    if sapling.state == "watered":
                        sapling.color = (0, 0, 255)
                    #sapling.texture = arcade.load_texture("path_to_watered_sapling_image.png")
                elif sapling.state == "watered":
                    sapling.state = "chopped"
                    #sapling.texture = arcade.load_texture("path_to_chopped_sapling_image.png")

                # Remove sapling if chopped
                if sapling.state == "chopped":
                    sapling.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        saplings_hit = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].sapling_list)

        if saplings_hit:
            print("Player is near a sapling! Press a key to interact.")

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()