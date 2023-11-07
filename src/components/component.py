import os

import pygame

import constants.game
import constants.headup
import utils.audio
import utils.image
import utils.quality
from constants.headup import UI_MARGIN


class Component(object):

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        self.data_dir = data_dir
        self.handle_change_component = handle_change_component
        self.image_cache = utils.image.ImageCache()
        self.settings_state = settings_state
        self.enable_edit_mode = enable_edit_mode
        self.gamepad = gamepad

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE)

        self.show_fps = None

    # Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(
            what,
            utils.quality.font_antialiasing(),
            pygame.Color(color)
        )

        self.screen.blit(text, where)

    def draw_notification(self, what, color, screen):
        """ Draw notification text in the bottom right of the screen"""
        text = self.monotype_font.render(
            what,
            utils.quality.font_antialiasing(),
            pygame.Color(color)
        )

        w, h = text.get_size()

        x, y = screen.get_size()

        x -= w
        y -= h

        y -= UI_MARGIN
        x -= UI_MARGIN

        where = (x, y)

        self.render_text(what, color, where)

    def tick_and_show_fps(self):
        if self.settings_state.show_fps and self.show_fps:
            self.show_fps()

    def update_screen(self, screen):
        screen.fill((0, 0, 0))

    def handle_event(self, event):
        return

    def set_screen(self, screen):
        self.screen = screen

    def mount(self):
        return

    def ai(self):
        return

    def play_music(self, file, repeat=-1):
        file = os.path.join(self.data_dir, 'music', file)
        utils.audio.play_music(file, repeat)

    def unmount(self):
        return True
