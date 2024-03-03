"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import logging
import os
import random

import arcade
from arcade import SpriteList, PymunkPhysicsEngine, FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

import constants.controls.controller
import constants.controls.keyboard
import sprites.characters.playersprite
import utils.audio
from sprites.bullet.bullet import Bullet
from sprites.bullet.grunt import Grunt
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.playersprite import PlayerSprite
from sprites.characters.skullsprite import SkullSprite
from sprites.items.coin import Coin
from sprites.ui.inventorycontainer import InventoryContainer
from utils.physics import make_physics_engine
from utils.sprite import random_position
from views.fading import Fading
from views.mainmenu import MainMenu
from views.pausemenu import PauseMenu

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

SPRITE_LIST_COINS = 'Coins'
SPRITE_LIST_WALL = 'Walls'
SPRITE_LIST_FENCE = 'Fence'
SPRITE_LIST_DECORATION = 'Decoration'
SPRITE_LIST_ENEMIES = 'Enemies'
SPRITE_LIST_PLAYER = 'player'
SPRITE_LIST_MOVEABLE = 'Moveable'
TOTAL_COINS = 100

# TODO: Make this dynamic
START_POS_X = 474
START_POS_Y = 852


class Game(Fading):
    """
    Main application class.
    """

    def __init__(self, window, state):

        # Call the parent class and set up the window
        super().__init__(window)

        self.state = state

        # Our TileMap Object
        self.tile_map = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # What key is pressed down?
        self.up_key_pressed = False
        self.right_key_pressed = False
        self.down_key_pressed = False
        self.left_key_pressed = False

        # Music queue
        self.music_queue = None

        # Inventory
        self.inventory = None

        self.initialized = False

        self.scene = arcade.Scene()

        self.message_box = None

    def on_show_view(self):
        super().on_show_view()
        print('view')
        print(self.window.controllers)
        self.window.set_mouse_visible(False)
        for controller in self.window.controllers:
            controller.push_handlers(self)

        if self.initialized:
            self.music_queue.play()
            return

        self.setup()
    def setup(self):

        # Set up the Cameras
        self.camera_sprites = arcade.Camera()

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, f"{self.state.map_name}.tmx")

        layer_options = {
            SPRITE_LIST_WALL: {
                "use_spatial_hash": True,
            },
            SPRITE_LIST_COINS: {
                "custom_class": Coin,
                "use_spatial_hash": True
            }
        }

        # Read in the tiled map
        try:
            self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options, use_spatial_hash=True)
        except FileNotFoundError as e:
            logging.error(e)
            arcade.exit()
            return

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'char', 'pig.png')
        self.player_sprite = PlayerSprite(filename)
        self.player_sprite.center_x = START_POS_X
        self.player_sprite.center_y = START_POS_Y
        self.scene.add_sprite(SPRITE_LIST_PLAYER, self.player_sprite)

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        # Create the music queue
        self.music_queue = utils.audio.MusicQueue(state=self.state)
        self.music_queue.from_directory(os.path.join(self.state.music_dir, self.state.map_name))
        self.music_queue.play()

        # Place coins
        for i in range(TOTAL_COINS):
            self.make_coin()

        self.initialized = True

        self.inventory = InventoryContainer()
        self.inventory.setup(state=self.state, size=self.window.size)

    def on_hide_view(self):
        self.music_queue.pause()
        for controller in self.window.controllers:
            controller.pop_handlers()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

        try:
            enemies = self.scene[SPRITE_LIST_ENEMIES]
        except KeyError:
            enemies = []
        for sprite in enemies:

            if self.window.debug:
                sprite.draw_debug()

            sprite.draw_overlay()

        self.camera_gui.use()

        self.inventory.draw()

        self.draw_fading()
        self.player_sprite.draw_overlay()
        self.draw_debug(self.player_sprite)


    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        move_force = self.player_sprite.move_force * self.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.up_key_pressed and not self.down_key_pressed:
            force_y = move_force
            self.player_sprite.change_y = -1
        elif self.down_key_pressed and not self.up_key_pressed:
            force_y = -move_force
            self.player_sprite.change_y = 1
        if self.left_key_pressed and not self.right_key_pressed:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.right_key_pressed and not self.left_key_pressed:
            force_x = move_force
            self.player_sprite.change_x = 1

        self.physics_engine.apply_force(self.player_sprite, (force_x, force_y))

    def reset_keys(self):
        # What key is pressed down?
        self.up_key_pressed = False
        self.right_key_pressed = False
        self.down_key_pressed = False
        self.left_key_pressed = False
        self.player_sprite.reset()

    def on_button_press(self, controller, key):
        logging.info(f"Controller button {key} pressed")
        if self.player_sprite.dead():
            if key in constants.controls.controller.KEY_DISCARD:
                self.next_view = MainMenu(self.window, self.state)
                self.fade_out()
            return

        if key in constants.controls.controller.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.controller.KEY_USE:
            self.on_use()
        if key in constants.controls.controller.KEY_DROP:
            self.on_drop()
        if key in constants.controls.controller.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.controller.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.controller.PREVIOUS_ITEM:
            self.on_select_item(index=self.inventory.previous())
        if key in constants.controls.controller.NEXT_ITEM:
            self.on_select_item(index=self.inventory.next())

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        if not self.initialized:
            return

        logging.info(f"Stick motion {stick_name}, {x_value}, {y_value}")

        x_value = round(x_value)
        y_value = round(y_value)

        if stick_name == constants.controls.controller.LEFTSTICK:
            if x_value == constants.controls.controller.AXIS_RIGHT:
                self.right_key_pressed = True
            elif x_value == constants.controls.controller.AXIS_LEFT:
                self.left_key_pressed = True
            else:
                self.right_key_pressed = False
                self.left_key_pressed = False

            if y_value == constants.controls.controller.AXIS_DOWN:
                self.down_key_pressed = True
            elif y_value == constants.controls.controller.AXIS_UP:
                self.up_key_pressed = True
            else:
                self.down_key_pressed = False
                self.up_key_pressed = False

        if stick_name == constants.controls.controller.RIGHTSTICK:
            face = self.player_sprite.face
            if x_value == constants.controls.controller.AXIS_RIGHT:
                face = FACE_RIGHT
            if x_value == constants.controls.controller.AXIS_LEFT:
                face = FACE_LEFT
            if y_value == constants.controls.controller.AXIS_DOWN:
                face = FACE_DOWN
            if y_value == constants.controls.controller.AXIS_UP:
                face = FACE_UP

            self.player_sprite.set_face(face)

    def on_trigger_motion(self, controller, trigger_name, value):
        logging.info(f"{trigger_name}, {value}")
        value = round(value)
        if trigger_name in constants.controls.controller.LEFT_TRIGGER:
            print(value)
            if value == constants.controls.controller.TRIGGER_ON:
                self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_SPRINT
            if value == constants.controls.controller.TRIGGER_OFF:
                self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_DEFAULT

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if self.player_sprite.dead():
            if key in constants.controls.keyboard.KEY_DISCARD:
                self.next_view = MainMenu(self.window, self.state)
                self.fade_out()

            return

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_SPRINT
        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()
        if key in constants.controls.keyboard.KEY_DROP:
            self.on_drop()
        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.left_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.right_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.up_key_pressed = True
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.down_key_pressed = True

        if key in constants.controls.keyboard.KEY_SELECT_INVENTORY:
            self.on_select_item(key=key)

    def on_key_release(self, key, modifiers):

        super().on_key_release(key, modifiers)
        """Called when the user releases a key."""

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = sprites.characters.playersprite.MODIFIER_DEFAULT

        movement = True

        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.left_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.right_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.up_key_pressed = False
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.down_key_pressed = False
        else:
            movement = False

        if movement:
            self.update_player_speed()

    def on_select_item(self, key=None, index=None):
        if key:
            index = constants.controls.keyboard.KEY_SELECT_INVENTORY.index(key)
            index -= 1

        item = self.inventory.select(index)
        self.player_sprite.set_item(item)
        if 'Place' in self.scene.name_mapping:
            self.scene.remove_sprite_list_by_name('Place')

        if not item:
            return

        self.scene.add_sprite('Place', item)

    def on_shoot(self):
        bullet = Bullet(6, color=arcade.csscolor.HOTPINK)
        bullet.setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_grunt(self):
        if self.state.is_silent():
            return

        bullet = Grunt(8)
        bullet.setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state,
        )

    def on_drop(self):
        item = self.player_sprite.get_item()
        selected, index = self.inventory.get_selected()
        if not item:
            logging.info('No item selected')
            self.state.sounds['beep'].play()
            return

        klass = item.__class__
        new_item = klass(filename=item.filename, center_x=item.center_x, center_y=item.center_y)
        layer = klass.__name__ + 's'

        if selected:
            quantity = selected.pop()

            if quantity == 0:
                self.player_sprite.set_item(None)
                self.inventory.unselect()

        self.scene.add_sprite(layer, new_item)

    def on_pause(self) -> None:
        """
        On show pause menu
        """
        self.reset_keys()
        self.window.show_view(PauseMenu(self.window, self.state, self))

    def on_use(self):
        if self.update_collectable():
            return

        logging.info('Nothing to use at ' + str(self.player_sprite.position))

        self.state.sounds['beep'].play()

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        if self.player_sprite.dead():
            self.update_fade(self.next_view)
            return

        # Move the player with the physics engine
        self.update_player()
        self.physics_engine.step()
        self.update_enemies(delta_time)
        self.center_camera_to_player()

        self.update_fade(self.next_view)

    def update_player(self):
        self.update_player_speed()
        self.player_sprite.update()

    def update_enemies(self, delta_time):
        try:
            enemies = self.scene[SPRITE_LIST_ENEMIES]
        except KeyError:
            enemies = []

        for sprite in enemies:
            if not isinstance(sprite, EnemySprite):
                continue
            sprite.update(
                player=self.player_sprite,
                scene=self.scene,
                physics_engine=self.physics_engine,
                state=self.state,
                delta_time=delta_time
            )

            if arcade.check_for_collision(sprite, self.player_sprite):
                self.player_sprite.hurt(sprite.damage)

        if len(enemies) < 5:
            if random.randint(1, 200) == 50:
                self.spawn_skull()
                logging.info(f'Spawn enemy, new total enemy count: {len(self.scene[SPRITE_LIST_ENEMIES])}')

    @property
    def all_layers(self):
        """ Returns all layers except background and decoration"""
        sprite_list = SpriteList(use_spatial_hash=False)

        layer_names = [
            SPRITE_LIST_WALL,
            SPRITE_LIST_COINS,
            SPRITE_LIST_ENEMIES,
            SPRITE_LIST_MOVEABLE,
            SPRITE_LIST_PLAYER,
            SPRITE_LIST_FENCE,
            SPRITE_LIST_DECORATION
        ]

        layers = []

        for layer_name in layer_names:
            try:
                layers.append(self.scene[layer_name])
            except KeyError:
                pass

        for layer in layers:
            for sprite in layer:
                sprite_list.append(sprite)

        return sprite_list

    def make_coin(self):
        rand_x, rand_y = random_position(self.tile_map)
        coin = Coin(
            filename=os.path.join(self.state.sprite_dir, 'coin', 'coin.png'),
            center_x=rand_x,
            center_y=rand_y
        )

        if arcade.check_for_collision_with_list(coin, self.all_layers):
            return self.make_coin()

        self.scene.add_sprite(SPRITE_LIST_COINS, coin)

        return

    def spawn_skull(self):
        rand_x, rand_y = random_position(self.tile_map)

        skull = SkullSprite(filename=os.path.join(self.state.sprite_dir, 'skull.png'), center_x=rand_x, center_y=rand_y)

        if arcade.check_for_collision_with_list(skull, self.all_layers):
            return

        self.scene.add_sprite(SPRITE_LIST_ENEMIES, skull)

        self.physics_engine.add_sprite(skull,
                                       friction=skull.friction,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="enemy",
                                       max_velocity=200,
                                       damping=skull.damping
                                       )

    def update_collectable(self):
        coins = arcade.check_for_collision_with_list(self.player_sprite, self.scene[SPRITE_LIST_COINS])
        # TODO: Use a hit handler of physics engine for this
        for coin in coins:
            self.scene[SPRITE_LIST_COINS].remove(coin)
            self.inventory.add_item(coin)
            self.state.play_sound('coin')
            self.on_select_item(index=-1)
            return True

        return False
