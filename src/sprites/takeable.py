""" Wall sprite """
import os

from sprites.sprite import Sprite
from utils.audio import play_sound


class Takeable(Sprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = True

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def handle_interact(self, element):
        """ Set walkable on interact """

        if not element.state.take_item(self):
            sound = os.path.abspath(
                os.path.join(
                    self.sprite_dir, '..',
                    '..',
                    'sounds',
                    'common',
                    'beep.ogg')
            )
            play_sound(sound)
            return

        self.purge = True

        sound = os.path.abspath(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'common',
                'pickup.ogg'
            )
        )
        play_sound(sound)
