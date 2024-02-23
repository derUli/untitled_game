"""
Grunzi game init file
"""
import gettext
import locale
import os

import arcade
import pyglet

from state.viewstate import ViewState
from views.mainmenuview import MainMenuView

ROOT_DIR = os.path.dirname(__file__)

# Set locale
locale_path = os.path.join(ROOT_DIR, 'data', 'locale')
os.environ['LANG'] = ':'.join(locale.getlocale())
gettext.install('messages', locale_path)

SCREEN_TITLE = _("Grunzi")

SCREEN = pyglet.canvas.get_display().get_default_screen()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10


class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE, fullscreen=True, vsync=True)


def main():
    """Main function"""
    window = GameWindow()
    state = ViewState(ROOT_DIR)
    view = MainMenuView(window, state)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
