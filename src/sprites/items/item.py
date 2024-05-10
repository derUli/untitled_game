import logging
from typing import Optional

import PIL
import arcade
from arcade import AnimatedTimeBasedSprite, FACE_RIGHT

from sprites.sprite import Sprite, AbstractStaticSprite, AbstractAnimatedSprite
from utils.positional_sound import PositionalSound


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
        )

    def on_use(self, b, state=None, handlers=None):
        logging.info(f"Use item {self} with {b}")

    def copy(self):
        logging.debug('Copy not implemented')
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


class Tree(Sprite, Useable):
    pass


class Jeep(Sprite, Useable):
    pass


class Water(AbstractAnimatedSprite):
    pass

FORCE_MOVE = 8000
HURT_PLAYER = 5

class Electric(AbstractAnimatedSprite):
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
        self.sound = None

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
        )

    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        if not self.sound:
            audio = state.play_sound('electric', 'on', loop=True)
            print(audio)
            self.sound = PositionalSound(player, self, audio, state)
            self.sound.play()

        self.sound.update()

        if arcade.check_for_collision(self, player):
            player.hurt(HURT_PLAYER)

            physics_engine.apply_force(player, (FORCE_MOVE, 0))
