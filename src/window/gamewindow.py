import logging

import arcade
import pyglet

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Grunzi"

UPDATE_RATE = 1 / 60
DRAW_RATE = 1 / 9999


class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(
            self,
            window=False,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            update_rate=UPDATE_RATE,
            draw_rate=DRAW_RATE,
            controller=False,
            vsync=None
    ):

        default_screen = pyglet.canvas.get_display().get_default_screen()
        native_mode = default_screen.get_mode()
        native_resolution = (native_mode.width, native_mode.height)
        style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
        self.is_native = native_resolution == (width, height)

        if not window and self.is_native:
            style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS

        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=SCREEN_TITLE,
            fullscreen=self.is_native,
            update_rate=update_rate,
            draw_rate=draw_rate,
            center_window=True,
            style=style,
            vsync=vsync
        )

        self.set_fullscreen(not window)

        self.update_rate = update_rate
        self.draw_rate = update_rate
        self.controller = controller
        self.controller_manager = None
        self.debug = False
        self.show_fps = False
        self.controllers = []

    def setup(self):
        # Enable timings for FPS measurements
        if not arcade.timings_enabled():
            arcade.enable_timings()

        # Init controllers if enabled
        self.init_controllers()

    def set_fullscreen(self, fullscreen=True):
        if self.is_native:
            return
        screen = pyglet.canvas.get_display().get_default_screen()
        mode = screen.get_closest_mode(self.width, self.height)

        return super().set_fullscreen(fullscreen=fullscreen, screen=screen, mode=mode)

    @property
    def size(self) -> tuple:
        """
        Size tuple of the window
        @return:
        """
        return self.width, self.height

    def init_controllers(self):
        if not self.controller:
            return

        try:
            self.controller_manager = pyglet.input.ControllerManager()

            for controller in self.controller_manager.get_controllers():
                logging.info(f'Controller: {controller.device.manufacturer} {controller.device.name}')
                controller.open(self)
                self.controllers.append(controller)
        except FileNotFoundError as e:
            logging.error(e)
            self.controllers = []
        finally:
            if not any(self.controllers):
                logging.info(f"No controllers detected")
