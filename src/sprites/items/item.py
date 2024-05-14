import logging
from typing import Optional

import PIL
import arcade
from arcade import FACE_RIGHT

from sprites.sprite import Sprite


class Item(Sprite):
    def __init__(
            self,
            filename: Optional[str] = None,
            image_x=0,
            image_y=0,
            image_width=None,
            image_height=None,
            flipped_horizontally=False,
            flipped_vertically=False,
            flipped_diagonally=False,
            hit_box_algorithm=None,
            hit_box_detail=None,
            scale=1.0,
            center_x=None,
            center_y=None
    ):
        self.filename = filename
        self.image = PIL.Image.open(filename).convert('RGBA').crop()

        self.images = self.generate_rotated(self.image)

        self._the_textures = []

        i = 0
        for image in self.images:
            self._the_textures.append(
                arcade.texture.Texture(name=str(filename) + str(i), image=image)
            )

            i += 1

        super().__init__(
            texture=self._the_textures[FACE_RIGHT - 1],
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            center_x=center_x,
            center_y=center_y
        )

    def on_use_with(self, b, state=None, handlers=None):
        logging.info(f"Use item {self} with {b}")

    def on_use(self, state, handlers):
        state.beep()

    def copy(self):
        logging.info('Copy not implemented')
        return self

    def draw_item(self, face):
        self.texture = self._the_textures[face - 1]
        self.draw()

    def generate_rotated(sel, image):
        return [
            image,
            PIL.ImageOps.mirror(image.copy()),
            image,
            image,
        ]


class Useable:
    """ Useable item"""
    pass


class Fence(Sprite, Useable):
    pass


class PiggyBank(Sprite, Useable):
    pass
