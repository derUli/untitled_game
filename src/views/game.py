"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import logging
import os
import random
import threading
import time

import pyglet.clock
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

import constants.controls.controller
import constants.controls.keyboard
import utils.audio
from constants.controls.joystick import JOYSTICK_BUTTON_MAPPING, AXIS_X, AXIS_Y
from constants.layers import *
from constants.maps import MAPS
from sprites.bullet.bullet import Bullet
from sprites.bullet.grunt import Grunt
from sprites.characters.character import Character
from sprites.characters.chicken import spawn_chicken
from sprites.characters.player import Player, MODIFIER_SPRINT, MODIFIER_DEFAULT
from sprites.characters.skull import spawn_skull
from sprites.decoration.sun import update_sun
from sprites.items.item import Item, Useable
from sprites.sprite import AbstractSprite
from sprites.ui.loadingscreen import LoadingScreen
from sprites.ui.uicontainer import UIContainer
from state.savegamestate import SaveGameState
from utils.callbackhandler import CallbackHandler
from utils.keypressed import KeyPressed
from utils.physics import make_physics_engine
from utils.positional_sound import PositionalSound
from utils.scene import get_layer
from utils.sprite import animated_in_sight
from utils.tilemap import TileMap
from utils.video import load_video
from views.camera import center_camera_to_player
from views.fading import Fading
from views.mainmenu import MainMenu
from views.pausemenu import PauseMenu
from window.gamewindow import UPDATE_RATE

COLOR_BACKGROUND = (70, 27, 27)


class Game(Fading):
    """
    Main application class.
    """

    def __init__(self, window, state, skip_intro=False):

        # Call the parent class and set up the window
        super().__init__(window)

        self.initialized = False

        self.state = state

        # Our TileMap Object
        self.tilemap = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # What key is pressed down?
        self.keypressed = KeyPressed()

        # Music queue
        self.music_queue = None
        self.atmo = None

        self.scene = None

        # This method is called in next call of on_update
        self._call_method = None

        self.video = None
        self.skip_intro = skip_intro

        self.ui = None
        self.loading_screen = None
        self.background = COLOR_BACKGROUND

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.window.set_mouse_visible(False)

        self.push_controller_handlers()

        self.state.settings.unmute()

        if self.initialized:
            self.music_queue.play()
            self.atmo.play()
            return

        self.setup()

    def on_hide_view(self) -> None:
        """ On hide view """
        super().on_hide_view()
        self.window.set_mouse_visible(True)
        self.music_queue.pause()
        self.pop_controller_handlers()
        self.atmo.pause()
        self.state.settings.mute()
        self.call_update(0)

    def setup(self) -> None:
        """ Setup game """

        video_file = os.path.join(self.state.video_dir, 'splash', f"{self.state.map_name}.webm")

        self.video = None

        if not self.skip_intro and self.state.settings.videos:
            self.video = load_video(
                video_file,
                self.window.size,
                self.state.settings.music_volume
            )

        self.loading_screen = LoadingScreen()
        self.loading_screen.setup(self.state, self.window.size)

        # Load map
        threading.Thread(target=self.async_load).start()

    def async_load(self) -> None:
        """ Async load map """

        start_time = time.time()

        self.loading_screen.percent = 0

        # Set up the Cameras
        self.camera_sprites = arcade.Camera()
        self.state.reset()

        self.loading_screen.percent = 10

        # Name of map file to load
        map_name = os.path.join(self.state.map_dir, f"{self.state.map_name}.tmx")

        # Read in the tiled map
        try:
            self.tilemap = TileMap(
                map_name,
                layer_options=LAYER_OPTIONS
            )
        except FileNotFoundError as e:
            logging.error(e)
            return arcade.exit()

        self.loading_screen.percent = 50

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tilemap.map)

        self.loading_screen.percent = 60

        # If the animated sky is disabled remove the sky layers
        if not self.state.settings.sky:
            for layer in SKY_LAYERS:
                if layer in self.scene.name_mapping:
                    self.scene.remove_sprite_list_by_name(layer)

        self.loading_screen.percent = 65

        if not self.state.settings.traffic:
            for layer in TRAFFIC_LAYERS:
                if layer in self.scene.name_mapping:
                    self.scene.remove_sprite_list_by_name(layer)

        self.loading_screen.percent = 70

        # Set up the player, specifically placing it at these coordinates.
        filename = os.path.join(self.state.sprite_dir, 'char', 'pig.png')
        self.player_sprite = Player(filename)

        self.player_sprite.setup(
            state=self.state,
            scene=self.scene,
            callbacks=CallbackHandler(
                on_complete=self.on_next_level
            )
        )

        self.loading_screen.percent = 75

        # Create the physics engine
        self.physics_engine = make_physics_engine(self.player_sprite, self.scene)

        self.loading_screen.percent = 80

        # Create the music queue
        self.music_queue = utils.audio.MusicQueue(state=self.state)
        self.music_queue.from_directory(os.path.join(self.state.music_dir, str(self.state.map_name)))

        self.loading_screen.percent = 85

        for i in range(random.randint(1, 4)):
            spawn_chicken(self.state, self.tilemap.map, self.scene, self.physics_engine)

        self.loading_screen.percent = 90

        self.ui = UIContainer()
        self.ui.setup(self.state, self.window.size)

        self.loading_screen.percent = 100

        pyglet.clock.schedule_interval_soft(self.wait_for_video, interval=UPDATE_RATE)

        # Sleep some seconds to wait until the 100 Percent is shown
        while not self.loading_screen.completed:
            time.sleep(0.01)

        self.initialized = True

        logging.info(f"Map {self.state.map_name} loaded in {time.time() - start_time} seconds")

    def wait_for_video(self, delta_time=0) -> None:
        """ Wait until video playback completed """

        self.window.set_mouse_visible(False)

        if not self.initialized:
            return

        # Wait until video is completed until playing music
        if self.video and self.video.active:
            return

        self.video = None

        self.music_queue.play()

        atmo = self.state.play_sound('atmos', self.state.map_name, loop=True)
        self.atmo = PositionalSound(self.player_sprite, self.player_sprite, atmo, self.state)

        pyglet.clock.unschedule(self.wait_for_video)

    def on_draw(self) -> None:
        """Render the screen."""

        if self.video and self.video.active:
            # Loading a video will open a ffmpeg console window.
            # Which will disappear after a second.
            # The game window lose it's focus.
            # Activate the window again.
            self.window.activate()

            self.video.draw((0, 0), force_draw=True)
            return self.draw_debug()

        self.clear()

        if not self.initialized or not self.loading_screen.completed:
            self.loading_screen.draw(time=self.time)

            return self.draw_debug()

        self.camera_sprites.use()
        self.scene.draw()

        for sprite in get_layer(LAYER_NPC, self.scene):

            if not isinstance(sprite, Character) and not isinstance(sprite, Bullet):
                continue

            sprite.draw_overlay()

            if self.window.debug:
                sprite.draw_debug()

        self.camera_gui.use()
        self.ui.draw()
        self.player_sprite.draw_overlay()
        self.draw_fading()
        self.draw_debug()

    def update_player_speed(self) -> None:
        """ Update player sprite """
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x, self.player_sprite.change_y = 0, 0

        move_force = self.player_sprite.move_force * self.player_sprite.modifier

        force_x, force_y = 0, 0

        if self.keypressed.key_up and not self.keypressed.key_down:
            force_y = move_force
            self.player_sprite.change_y = -1
        elif self.keypressed.key_down and not self.keypressed.key_up:
            force_y = -move_force
            self.player_sprite.change_y = 1
        if self.keypressed.key_left and not self.keypressed.key_right:
            force_x = -move_force
            self.player_sprite.change_x = -1
        elif self.keypressed.key_right and not self.keypressed.key_left:
            force_x = move_force
            self.player_sprite.change_x = 1

        if force_x != 0 or force_y != 0:
            self.player_sprite.start_walk(sprint=self.player_sprite.sprinting)
            self.window.set_mouse_visible(False)
        else:
            self.player_sprite.stop_walk()

        self.physics_engine.apply_force(self.player_sprite, (force_x, force_y))

    def on_button_press(self, controller, key):
        logging.info(f"Controller button {key} pressed")

        if not self.initialized:
            return

        if self.video and self.video.active:
            if key in constants.controls.controller.KEY_DISCARD:
                self.video.stop()
            return

        if self.player_sprite.dead:
            if key in constants.controls.controller.KEY_DISCARD:
                self._call_method = self.on_gameover
            return

        if key in constants.controls.controller.KEY_PAUSE:
            self._call_method = self.on_pause
        if key in constants.controls.controller.KEY_USE:
            self._call_method = self.on_use
        if key in constants.controls.controller.KEY_DROP:
            self._call_method = self.on_drop
        if key in constants.controls.controller.KEY_SHOOT:
            self._call_method = self.on_shoot
        if key in constants.controls.controller.KEY_GRUNT:
            self._call_method = self.on_grunt
        if key in constants.controls.controller.PREVIOUS_ITEM:
            self._call_method = self.on_item_previous
        if key in constants.controls.controller.NEXT_ITEM:
            self._call_method = self.on_item_next
        if key in constants.controls.controller.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_SPRINT

    def on_joybutton_press(self, controller, key):
        if str(key) in JOYSTICK_BUTTON_MAPPING:
            button = JOYSTICK_BUTTON_MAPPING[str(key)]
            self.on_button_press(controller, button)

    def on_button_release(self, controller, key):
        logging.info(f"Controller button {key} released")

        if not self.initialized:
            return

        if self.video and self.video.active:
            return

        if key in constants.controls.controller.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_DEFAULT

    def on_joybutton_release(self, controller, key):
        if str(key) in JOYSTICK_BUTTON_MAPPING:
            button = JOYSTICK_BUTTON_MAPPING[str(key)]
            self.on_button_release(controller, button)

    def on_item_previous(self):
        self.on_select_item(index=self.ui.inventory.previous())

    def on_item_next(self):
        self.on_select_item(index=self.ui.inventory.next())

    def on_main_menu(self):
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_gameover(self):
        self.on_next_level(same=True)

    def on_next_level(self, same=False):
        self.player_sprite.reset()

        if self.next_view:
            return

        old_map = self.state.map_name
        next_map = old_map
        index = MAPS.index(old_map)

        if not same:
            index += 1

        completed = False

        try:
            next_map = MAPS[index]
        except IndexError as e:
            logging.error(e)
            completed = True

        self.state.map_name = next_map

        savegame = SaveGameState.load()
        savegame.current = next_map
        savegame.completed += [old_map]
        savegame.score[old_map] = self.state.score
        savegame.save()

        if completed:
            logging.info('Game Completed')
            logging.info('TODO: Implement outro')
            return

        self.next_view = Game(self.window, self.state, skip_intro=same)
        self.fade_out()

    def on_stick_motion(self, controller, stick_name, x_value, y_value):
        logging.info(f"Stick motion {stick_name}, {x_value}, {y_value}")

        if not self.initialized:
            return

        if self.video and self.video.active:
            return

        x_value, y_value = round(x_value), round(y_value)

        if stick_name == constants.controls.controller.LEFTSTICK:
            if x_value == constants.controls.controller.AXIS_RIGHT:
                self.keypressed.key_right = True
            elif x_value == constants.controls.controller.AXIS_LEFT:
                self.keypressed.key_left = True
            else:
                self.keypressed.key_right = False
                self.keypressed.key_left = False

            if y_value == constants.controls.controller.AXIS_DOWN:
                self.keypressed.key_down = True
            elif y_value == constants.controls.controller.AXIS_UP:
                self.keypressed.key_up = True
            else:
                self.keypressed.key_down = False
                self.keypressed.key_up = False

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

    def on_joyaxis_motion(self, joystick, axis, value):
        value = round(value)

        x_value, y_value = 0, 0

        if axis == AXIS_X:
            x_value = round(value)

        if axis == AXIS_Y:
            y_value = round(value) * - 1

        self.on_stick_motion(joystick, constants.controls.controller.LEFTSTICK, x_value, y_value)

    def on_trigger_motion(self, controller, trigger_name, value):
        logging.info(f"{trigger_name}, {value}")

        if not self.initialized:
            return

        if self.video and self.video.active:
            return

        value = round(value)

        if trigger_name in constants.controls.controller.LEFT_TRIGGER:
            if value == constants.controls.controller.TRIGGER_ON:
                self.player_sprite.modifier = MODIFIER_SPRINT
            if value == constants.controls.controller.TRIGGER_OFF:
                self.player_sprite.modifier = MODIFIER_DEFAULT

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if self.video and self.video.active:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.video.stop()

        if not self.initialized:
            return

        if self.player_sprite.dead:
            if key in constants.controls.keyboard.KEY_DISCARD:
                return self.on_gameover()

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_pause()
        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_SPRINT
        if key in constants.controls.keyboard.KEY_USE:
            self.on_use()
        if key == arcade.key.F2:
            self.on_next_level()
        if key in constants.controls.keyboard.KEY_DROP:
            self.on_drop()
        if key in constants.controls.keyboard.KEY_SHOOT:
            self.on_shoot()
        if key in constants.controls.keyboard.KEY_GRUNT:
            self.on_grunt()
        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.keypressed.key_left = True
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.keypressed.key_right = True
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.keypressed.key_up = True
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.keypressed.key_down = True
        if key in constants.controls.keyboard.KEY_SELECT_INVENTORY:
            self.on_select_item(key=key)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        super().on_key_release(key, modifiers)

        if not self.initialized:
            return

        if self.video and self.video.active:
            return

        if key in constants.controls.keyboard.KEY_SPRINT:
            self.player_sprite.modifier = MODIFIER_DEFAULT

        movement = True

        if key in constants.controls.keyboard.KEY_MOVE_LEFT:
            self.keypressed.key_left = False
        elif key in constants.controls.keyboard.KEY_MOVE_RIGHT:
            self.keypressed.key_right = False
        elif key in constants.controls.keyboard.KEY_MOVE_UP:
            self.keypressed.key_up = False
        elif key in constants.controls.keyboard.KEY_MOVE_DOWN:
            self.keypressed.key_down = False
        else:
            movement = False

        if movement:
            self.update_player_speed()
        else:
            self.player_sprite.stop_walk()

    def on_select_item(self, key=None, index=None):
        old_item = self.player_sprite.get_item()

        if key:
            index = constants.controls.keyboard.KEY_SELECT_INVENTORY.index(key)
            index -= 1

        item = self.ui.inventory.select(index)
        self.player_sprite.set_item(item)

        if old_item:
            old_item.remove_from_sprite_lists()

        if not item:
            return

        self.scene.add_sprite(LAYER_PLACE, item)

    def on_shoot(self):
        return Bullet(6, color=arcade.csscolor.HOTPINK).setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            state=self.state,
            scene=self.scene
        )

    def on_grunt(self):
        return Grunt(8).setup(
            source=self.player_sprite,
            physics_engine=self.physics_engine,
            scene=self.scene,
            state=self.state
        )

    def on_drop(self):
        item = self.player_sprite.get_item()
        selected, index = self.ui.inventory.get_selected()
        if not item:
            logging.info('No item selected')
            return self.state.beep()

        klass = item.__class__
        # FIXME: Layer names should match the class names
        layer = klass.__name__
        new_item = item.copy()

        # TODO: Make a method for collision checks with multiple players
        if check_collision_with_layers(self.scene, new_item, WALL_LAYERS):
            logging.info("Can't drop item on wall.")
            self.state.beep()
            return

        if selected:
            quantity = selected.pop()

            if quantity == 0:
                self.player_sprite.set_item(None)
                self.ui.inventory.unselect()

        self.scene.add_sprite(layer, new_item)

    def on_pause(self) -> None:
        """
        On show pause menu
        """

        self.keypressed.reset()
        self.player_sprite.reset()

        menu = PauseMenu(self.window, self.state, self)
        menu.setup()
        self.window.show_view(menu)

    def on_use(self):
        if not self.player_sprite.get_item():
            return self.update_collectable()

        item = self.player_sprite.get_item()
        sprites = arcade.check_for_collision_with_lists(self.player_sprite.get_item(), self.scene.sprite_lists)

        for sprite in sprites:
            if isinstance(sprite, Useable):
                item.on_use_with(
                    sprite,
                    state=self.state,
                    handlers=CallbackHandler(on_complete=self.on_next_level)
                )
                return

        item.on_use(
            state=self.state,
            handlers=CallbackHandler(on_complete=self.on_next_level)
        )

    def on_update(self, delta_time):
        """Movement and game logic"""

        super().on_update(delta_time)

        self.time += delta_time

        self.loading_screen.update()

        if not self.initialized:
            return

        if self.video and self.video.active:
            return

        if self.atmo:
            self.atmo.update()

        if self.music_queue:
            self.music_queue.update()

        # There is an OpenGL error happens when a sprite is added by an controller event handler
        # which seems to happen because the controller events are handled in a different thread.
        # To work around this we have the _call_method class variable which can be set to a class method
        # Which is called in next execution of on_update
        if self._call_method:
            self._call_method()
            self._call_method = None

        if self.player_sprite.dead:
            self.player_sprite.reset()
            return self.update_fade(self.next_view)

        # Move the player with the physics engine
        self.update_player_speed()
        self.physics_engine.step()
        self.call_update(delta_time)
        self.update_enemies(delta_time)
        center_camera_to_player(self.player_sprite, self.camera_sprites, self.tilemap.size)
        update_sun(self.scene, self.camera_sprites)

        # Animate only visible
        animated = animated_in_sight(self.scene, self.player_sprite)
        for sprite in animated:
            sprite.update_animation(delta_time)

        self.update_fade(self.next_view)

    def call_update(self, delta_time):
        for sprite_list in self.scene.sprite_lists:
            for sprite in sprite_list:

                if not isinstance(sprite, AbstractSprite):
                    continue

                sprite.update(
                    player=self.player_sprite,
                    scene=self.scene,
                    physics_engine=self.physics_engine,
                    state=self.state,
                    delta_time=delta_time,
                    map_size=self.tilemap.size
                )

    def update_enemies(self, delta_time):
        enemies = get_layer(LAYER_NPC, self.scene)

        if len(enemies) < self.state.difficulty.max_skulls:
            a, b = self.state.difficulty.skull_spawn_range
            if random.randint(a, b) == 50:
                spawn_skull(self.state, self.tilemap.map, self.scene, self.physics_engine)

    def update_collectable(self):
        items = arcade.check_for_collision_with_lists(self.player_sprite, self.scene.sprite_lists)
        for item in items:
            if isinstance(item, Item):
                item.remove_from_sprite_lists()

                self.ui.inventory.add_item(item)
                self.state.play_sound('coin')
                self.on_select_item(index=-1)
                return True

        self.state.beep()
        return False
