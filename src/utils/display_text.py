import logging
import os
import time

import pygame

from constants.game import TEXT_FONT_SIZE, MONOTYPE_FONT
from utils.quality import font_antialiasing_enabled

TEXT_COLOR = (255, 255, 255)
TIME_PER_CHAR = 0.2
TIME_MIN = 1
MIN_FONT_SIZE = 12


class DisplayText:
    def __init__(self, data_dir):
        self.font = os.path.join(data_dir, 'fonts', MONOTYPE_FONT)
        self.rendered_text = None
        self.show_end = 0

    def draw(self, screen, pos):
        if not self.rendered_text:
            return

        if time.time() > self.show_end:
            self.rendered_text = None
            return

        screen.blit(self.rendered_text, pos)

    def show_text(self, what, fit_width=450):
        logging.info(what)
        original_what = what

        font_size = TEXT_FONT_SIZE

        rendered_text = None

        actual_width = fit_width + 1

        while actual_width > fit_width:
            font = pygame.font.Font(
                self.font,
                font_size
            )

            text = what
            if what != original_what:
                text += "..."

            rendered_text = font.render(
                text,
                font_antialiasing_enabled(),
                TEXT_COLOR
            ).convert_alpha()

            actual_width = rendered_text.get_width()

            font_size -= 1

            if font_size < MIN_FONT_SIZE:
                what = what[:-3]
                font_size = TEXT_FONT_SIZE

        self.rendered_text = rendered_text

        show_time = len(what) * TIME_PER_CHAR
        if show_time < TIME_MIN:
            show_time = TIME_MIN

        self.show_end = time.time() + show_time
