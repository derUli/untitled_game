import time

import arcade

from state.viewstate import ViewState
from utils.text import create_text, MARGIN, EXTRA_LARGE_FONT_SIZE

BAR_HEIGHT = 30


class LoadingScreen:
    def __init__(self):
        self.size = None
        self.shadertoy = None

        self.loading_text = None
        self.time = 0

        self.onepercent = None
        self._percent = 0
        # TODO: Progress bar

    def setup(self, state: ViewState, size: tuple):
        if state.settings.shaders:
            self.shadertoy = state.load_shader(size, 'gameover')

        w, h = size
        self.size = size

        self.onepercent = w / 100

        self.loading_text = create_text(
            _("Loading..."),
            width=w - (MARGIN * 2),
            font_size=EXTRA_LARGE_FONT_SIZE,
            align='left'
        )

        self._percent = 0
        self.loading_text.x = w / 2 - self.loading_text.content_width / 2
        self.loading_text.y = h / 2 - self.loading_text.content_height / 2

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        if value <= 0:
            value = 0

        if value > 100:
            value = 100

        self._percent = value

    def draw(self, time=None):
        if self.shadertoy:
            self.shadertoy.render(time=time)

        bar_width = self._percent * self.onepercent

        arcade.draw_rectangle_filled(
            bar_width / 2,
            BAR_HEIGHT / 2,
            bar_width,
            BAR_HEIGHT,
            arcade.csscolor.HOTPINK
        )

        self.loading_text.draw()
