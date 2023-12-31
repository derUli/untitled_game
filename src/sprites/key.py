""" Wall sprite """
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable


class Key(Takeable, InlineSprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='key1.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
