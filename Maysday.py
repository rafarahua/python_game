import arcade
import os
import math
import random

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

maze_width = 14
maze_height = 10

SCREEN_WIDTH = SPRITE_SIZE * maze_width
SCREEN_HEIGHT = SPRITE_SIZE * maze_height
SCREEN_TITLE = "Maysday"

MOVEMENT_SPEED = 5

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        self.wall_list = None
        self.background = None

        # Initialize sapling list
        self.sapling_list = arcade.SpriteList()

         # New dirt_patch_list attribute to hold dirt patch locations
        self.dirt_patch_list = arcade.SpriteList()

        self.bed_list = arcade.SpriteList()  # List to hold bed

        # Message for collecting saplings.
        self.sapling_message = None
        self.message_duration = 0

class Sapling(arcade.Sprite):
    def __init__(self, image_collected, image_planted, image_watered, image_grown, scale=0.5):
        super().__init__(image_collected, scale)
        
        # Initialize backing variables for properties
        self._center_x = super().center_x  # Initialize with the default position
        self._center_y = super().center_y  # Initialize with the default position
        
        self.image_collected = image_collected
        self.image_planted = image_planted
        self.image_watered = image_watered
        self.image_grown = image_grown
        self.state = "collected"
        self.plant_position = None
        self.dirt_patch = None

    @property
    def center_x(self):
        return self._center_x
    
    @center_x.setter
    def center_x(self, value):
        self._center_x = value
        super().set_position(value, self._center_y)

    @property
    def center_y(self):
        return self._center_y

    @center_y.setter
    def center_y(self, value):
        self._center_y = value
        super().set_position(self._center_x, value)

    def plant(self, x, y, dirt_patch):
        """Transition to 'planted' state and set position."""
        self.state = "planted"
        self.center_x = x
        self.center_y = y
        self.dirt_patch = dirt_patch
        self.texture = arcade.load_texture(self.image_planted)

    def water(self):
        """Transition to 'watered' state and update the image."""
        if self.state == "planted":
            self.state = "watered"
            self.texture = arcade.load_texture(self.image_watered)
            if self.dirt_patch:
                self.dirt_patch.water()

    def grow(self):
        """Transition to 'grown' state after watering and a 'day' passes."""
        if self.state == "watered":
            self.state = "grown"
            self.texture = arcade.load_texture(self.image_grown)
            self.scale *= 4.5
            if self.dirt_patch:
                self.dirt_patch.dry()

class DirtPatch(arcade.Sprite):
    """A class for designated planting areas with no collision."""

    def __init__(self, x, y, scale=SPRITE_SCALING):
        super().__init__("textures/PPFE/tile_0000.png", scale)
        self.center_x = x
        self.center_y = y
        self.is_planted = False  # Track if this patch is occupied by a sapling

    def water(self):
        """Darken the patch to indicate it has been watered."""
        self.color = (139, 69, 19)

    def dry(self):
        self.color = (255, 255, 255)

class Bed(arcade.Sprite):
    """ A class for the bed. """
    def __init__(self, x, y, scale=SPRITE_SCALING):
        super().__init__("textures/PPFE/pngwing.com.png", scale=0.035)
        self.center_x = x
        self.center_y = y

def setup_room_1():
    """
    Create and return room 1.
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

    # Generating saplings
    initial_saplings = random.randint(1, 3)

    # Generate all positions in the maze
    all_positions = [(x, y) for x in range(1, maze_width-1) for y in range(1, maze_height-1)]

    # Remove wall positions to get open spaces
    open_positions = [pos for pos in all_positions if pos not in wall_positions]

    chosen_positions = random.sample(open_positions, initial_saplings)
    print(chosen_positions)

    # Place saplings in open positions
    for x, y in chosen_positions:
        sapling = Sapling(
            image_collected=":resources:images/tiles/mushroomRed.png",
            image_planted="textures/PPFE/tile_0075.png",
            image_watered="textures/PPFE/tile_0075.png",
            image_grown="textures/PPFE/tile_0057.png",
            scale=SPRITE_SCALING
        )
        # Position the sapling using the chosen coordinates
        sapling.center_x = x * SPRITE_SIZE + 30  # Adjust offset if needed
        sapling.center_y = y * SPRITE_SIZE + 50  # Adjust offset if needed
        room.sapling_list.append(sapling)

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
    room.sapling_list = arcade.SpriteList()
    room.dirt_patch_list = arcade.SpriteList()

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

    # DirtPatch positions
    dirt_patch_positions = [
        (10*SPRITE_SIZE, 7*SPRITE_SIZE), (11*SPRITE_SIZE, 7*SPRITE_SIZE),
        (10*SPRITE_SIZE, 6*SPRITE_SIZE), (11*SPRITE_SIZE, 6*SPRITE_SIZE),
        (10*SPRITE_SIZE, 5*SPRITE_SIZE), (11*SPRITE_SIZE, 5*SPRITE_SIZE),
    ]

    # Create DirtPatches
    for position in dirt_patch_positions:
        dirt_patch = DirtPatch(position[0], position[1], scale=3)
        room.dirt_patch_list.append(dirt_patch)

    room.background = arcade.load_texture("textures/Backgrounds/Grass.png")

    # Add the bed
    bed = Bed(10.5 * SPRITE_SIZE, 8.5 * SPRITE_SIZE)  # Position the bed
    room.bed_list.append(bed)

    return room


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)
        self.sapling_inventory = [] 
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Simple small toolbar, with either watering can or axe.
        self.current_tool = "watering_can"  # Start with the watering can selected
        self.hotbar_icons = {
            "watering_can": "textures/PPFE/tile_0026.png",
            "shovel": "textures/PPFE/tile_0037.png"
        }
        self.hotbar_textures = {
            "watering_can": arcade.load_texture(self.hotbar_icons["watering_can"]),
            "shovel": arcade.load_texture(self.hotbar_icons["shovel"])
        }
        self.sapling_counter = 0

        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

        self.sapling_icon = arcade.load_texture(":resources:images/tiles/mushroomRed.png")
        self.tomato_icon = arcade.load_texture("textures/PPFE/tile_0057.png")
        self.tomato_counter = 0

        # Day change text
        self.current_day = 1  # Initialize current day
        self.day_message = ""  # Message to display for the day
        self.show_day_message = False  # Flag to control message visibility
        self.message_timer = 0  # Timer for how long to show the message
        self.fade_duration = 3.0
        self.fade_out = 1.0

        # Collecting sapling
        self.sapling_message = None  # Message for sapling collection
        self.message_duration = 0  # Duration for which to show the message
        self.message_position = (0, 0)  # Position of the message

        

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
         # Draw dirt patches (planting zones)
        self.rooms[self.current_room].dirt_patch_list.draw()
        
        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # Draw the bed
        self.rooms[self.current_room].bed_list.draw()

        # Draw the hotbar at the bottom center of the screen
        hotbar_x = SCREEN_WIDTH // 2
        hotbar_y = 30  # Position at the bottom of the screen

        for idx, tool in enumerate(self.hotbar_icons):
            icon_x = hotbar_x + (idx - 0.5) * 65  # Adjust positions for multiple items

            # Draw the icon
            arcade.draw_texture_rectangle(
                icon_x, hotbar_y,
                50, 50,
                self.hotbar_textures[tool]
            )

            # Highlight the selected tool
            if tool == self.current_tool:
                arcade.draw_rectangle_outline(icon_x, hotbar_y, 60, 60, arcade.color.YELLOW, 3)

        if self.show_day_message:
            arcade.draw_text(self.day_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, 20, anchor_x="center", anchor_y="center")
    

        # Draw saplings
        self.rooms[self.current_room].sapling_list.draw()

        self.player_list.draw()

        self.draw_sapling_counter()

        # Sapling Collection message in room 1
        if self.sapling_message:
            arcade.draw_text (self.sapling_message, self.message_position[0], self.message_position[1],
                              arcade.color.WHITE, 18, anchor_x="center", anchor_y="bottom")

        # Draw the day message with fade out
        if self.day_message:
            alpha_value = int(255 * self.fade_out)
            arcade.draw_text(self.day_message, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             (255,255,255, alpha_value), #RGB ans alpha (opacity)
                             20, anchor_x="center", anchor_y="center")

    
    def draw_sapling_counter(self):
        # Position to draw the icon and counter
        icon_x = 30  # X position for the icon
        icon_y = self.height - 10  # Y position for the icon

        # Draw a background rectangle for the sapling count
        box_width = 180  # Width of the box
        box_height = 30  # Height of the box
        box_x = icon_x - 20 + box_width / 2  # Centered box position
        box_y = icon_y - 15  # Positioning the box with the text

        # Draw the sapling icon
        arcade.draw_texture_rectangle(icon_x + box_width*3/5, icon_y, 50, 50, self.sapling_icon)

        arcade.draw_lrtb_rectangle_outline(box_x - box_width / 2, box_x + box_width / 2, 
                                            box_y + box_height / 2, box_y - box_height / 2, 
                                            arcade.color.WHITE)  # Draw the background box

        # Draw the sapling count text
        arcade.draw_text(f"Saplings       {self.sapling_counter}", 
                        icon_x - 15, icon_y - 20, arcade.color.WHITE, 18)
        
        # Tomato counter box (positioned below sapling counter)
        if self.tomato_counter >= 1:
            tomato_y = icon_y - 60  # Offset below sapling counter
            tomato_box_y = box_y - 60

            # Draw the tomato icon and counter
            arcade.draw_texture_rectangle(icon_x + box_width*3/5, tomato_box_y, 25, 25, self.tomato_icon)
            arcade.draw_lrtb_rectangle_outline(box_x - box_width / 2, box_x + box_width / 2, 
                                         tomato_box_y + box_height / 2, tomato_box_y - box_height / 2, 
                                         arcade.color.WHITE)
            arcade.draw_text(f"Tomatoes      {self.tomato_counter}", 
                        icon_x - 15, tomato_y - 20, arcade.color.WHITE, 18)

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
            print(f"Selected tool: {self.current_tool}")
        elif key == arcade.key.KEY_2:
            self.current_tool = "shovel"
            print(f"Selected tool: {self.current_tool}")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        saplings_hit = []
        # Check if we can collect a sapling

        for sapling in self.rooms[self.current_room].sapling_list:
            distance_to_player = math.sqrt((self.player_sprite.center_x - sapling.center_x) ** 2 + (self.player_sprite.center_y - sapling.center_y) ** 2)
            distance_to_click = math.sqrt((x - sapling.center_x) ** 2 + (y - sapling.center_y) ** 2)

            print(f"Sapling Position: {sapling.center_x}, {sapling.center_y}")  # Print sapling position for DEBUG

            if distance_to_player < 80 and distance_to_click < 50:  # Adjust these values to tweak distance to sapling
                saplings_hit.append(sapling)

        if saplings_hit:
            print("Sapling interacted with!")
            for sapling in saplings_hit:
                if not hasattr(sapling, "state"):
                    sapling.state = "default"

                # Change sapling state based on interaction
                if self.current_tool == "watering_can":
                    sapling.water()

                if self.current_tool == "shovel" and sapling.state != "dug":
                    if sapling.state == "grown":
                        self.tomato_counter += 1
                        print(f"Tomato counter: {self.tomato_counter}")
                    else: self.dig_sapling()

                    if sapling.dirt_patch:
                        sapling.dirt_patch.is_planted = False

                    sapling.remove_from_sprite_lists()

                    # Set message for sapling collection
                    if self.current_room == 0:  # Check if in room 1
                        self.sapling_message = "Mystery sapling collected"
                    elif self.current_room == 1:
                        if sapling.state == "grown":
                            self.sapling_message = "Tomato collected"
                        else:
                            self.sapling_message = "Sapling collected"
                    self.message_duration = 2  # Set duration for the message
                    self.message_position = (sapling.center_x, sapling.center_y)  # Position above sapling
                    saplings_hit.clear()              

        # Check if we can plant a sapling on a dirt patch
        if self.sapling_counter > 0 and self.current_tool == "shovel":
            for dirt_patch in self.rooms[self.current_room].dirt_patch_list:
                distance_to_patch = math.sqrt(
                    (x - dirt_patch.center_x) ** 2 + (y - dirt_patch.center_y) ** 2
                )

                # If within planting range, plant a sapling at this dirt patch
                if distance_to_patch < 10 and not dirt_patch.is_planted:
                    # Decrease sapling counter
                    self.sapling_counter -= 1


                    # Create a new sapling at this patch position in "planted" state
                    sapling = Sapling(
                        image_collected=":resources:images/tiles/mushroomRed.png",
                        image_planted="textures/PPFE/tile_0075.png", 
                        image_watered="textures/PPFE/tile_0075.png",
                        image_grown="textures/PPFE/tile_0057.png", 
                        scale=SPRITE_SCALING
                    )
                    sapling.plant(dirt_patch.center_x, dirt_patch.center_y, dirt_patch)
                    self.rooms[self.current_room].sapling_list.append(sapling)
                    dirt_patch.is_planted = True  # Mark patch as occupied
                    print("Sapling planted on dirt patch!")
                    return  # Exit after planting
                
        # Check if we can go to bed (interact with the bed)        
        for bed in self.rooms[self.current_room].bed_list:
            distance_to_bed = math.sqrt(
                (x - bed.center_x) ** 2 + (y - bed.center_y) ** 2
            )
            # If within interaction range of the bed, start a new day
            if distance_to_bed < 80:
                self.current_day += 1  # Increment day count
                self.day_message = f"Good morning!\nDay {self.current_day}"  # Set message
                self.show_day_message = True  # Trigger message display
                self.message_timer = 3  # Set duration to show message
                self.respawn_saplings_room0()
                print("Going to bed for the night!")
                self.grow_saplings()  # Check for growing saplings
                return
    def respawn_saplings_room0(self):
        """Respawn saplings in room 0 at the start of the day at random locations"""
        self.rooms[0].sapling_list = arcade.SpriteList() # Clear the sapling list
        
        daily_saplings = random.randint(1, 3)
        print(f"Daily saplings: {daily_saplings}")

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

        # Find open positions in maze for saplings to grow
        all_positions = [(x,y) for x in range(1, maze_width-1) for y in range(1, maze_height-1)]
        open_positions = [pos for pos in all_positions if pos not in wall_positions]
        chosen_positions = random.sample(open_positions, daily_saplings)

        for x, y in chosen_positions:
            sapling = Sapling(image_collected=":resources:images/tiles/mushroomRed.png",
                              image_planted="textures/PPFE/tile_0075.png",
                              image_watered="textures/PPFE/tile_0075.png",
                              image_grown="textures/PPFE/tile_0057.png",
                              scale=SPRITE_SCALING)
            sapling.center_x = x * SPRITE_SIZE + 30
            sapling.center_y = y * SPRITE_SIZE + 50

            self.rooms[0].sapling_list.append(sapling)
    def grow_saplings(self):
        for sapling in self.rooms[self.current_room].sapling_list:
            print(sapling.state)
            if sapling.state == "watered":
                sapling.grow()
                print("Sapling grew!")

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        saplings_hit = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].sapling_list)

        if self.show_day_message:
            self.message_timer -= delta_time

            # Decrease fade_out value for fade effect:
            if self.message_timer >0:
                self.fade_out = 1.0
            else:
                self.fade_out = max(0, self.message_timer/3)

            # Hide the message after 3 seconds
            if self.fade_out <=0:
                self.show_day_message = False

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
        
        # Collecting sapling in room 1 message
        if self.message_duration >0:
            self.message_duration -= delta_time
            if self.message_duration <=0:
                self.sapling_message = None

    def dig_sapling(self):
        self.sapling_counter += 1
        print(f"Saplings collected: {self.sapling_counter}")

def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()