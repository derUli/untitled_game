import logging

from sprites.ui.uicontainer import UIContainer
from utils.loader.loader import Loader
from utils.media.video import Video
from views.fading import Fading
from views.menu.mainmenu import MainMenu


class Game(Fading):
    def __init__(self, window, state, skip_intro=False):

        # Call the parent class and set up the window
        super().__init__(window)

        self.initialized = False

        self.state = state

        # Our TileMap Object
        self.tilemap = None

        # Separate variable that holds the player sprite
        self.scene.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # Music queue
        self.music_queue = None
        self.atmo = None
        self.loading_music = None

        # This method is called in next call of on_update
        self._call_method = None

        self.video = Video(None)
        self.skip_intro = skip_intro

        self.ui = None
        self.level_completed = False

        self.astar_barrier_list = None
        self.wall_spritelist = None
        self.map_populator = None

    def setup(self):
        self.initialized = False
        self.loading_music = None

        self.ui = UIContainer()
        self.ui.setup(self.state, self.window.size)

        self.level_completed = False
        # Load map
        Loader(self).load_async()

    @property
    def input_ready(self) -> bool:
        """ Check if the game is ready to handle input """

        if not self.initialized:
            return False

        return not self.video.active

    def on_gameover(self):
        logging.warning('TODO: implement on_gameover()')