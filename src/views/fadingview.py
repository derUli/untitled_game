import arcade

from views.view import View

FADE_RATE = 5


class FadingView(View):
    def __init__(self, window):
        super().__init__(window)
        self._fade_out = None
        self._fade_in = 255
        self._do_quit = False

    def update_fade(self, next_view=None):
        if self._fade_out is not None:
            self._fade_out += FADE_RATE
            if self._fade_out is not None and self._fade_out > 255 and next_view is not None:
                self.window.show_view(next_view)

            if self._fade_out is not None and self._fade_out > 255 and self._do_quit:
                arcade.exit()

        if self._fade_in is not None:
            self._fade_in -= FADE_RATE
            if self._fade_in <= 0:
                self._fade_in = None

    def fade_out(self):
        self._fade_out = 0
        self._fade_in = None

    def draw_fading(self):
        if self._fade_out is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self._fade_out))

        if self._fade_in is not None:
            arcade.draw_rectangle_filled(self.window.width / 2, self.window.height / 2,
                                         self.window.width, self.window.height,
                                         (0, 0, 0, self._fade_in))

    def fade_quit(self):
        self.fade_out()
        self._do_quit = True