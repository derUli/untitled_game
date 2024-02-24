""" Player sprite class """

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

import utils.text

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 3000
MOVE_DAMPING = 0.01

HEALTH_FULL = 100.0
HEALTH_EMPTY = 0.0
HEALTH_REGENERATION_SPEED = 0.1

FULL_ALPHA = 255
ONE_PERCENT_ALPHA = FULL_ALPHA / 100


class PlayerSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        self.move_force = MOVE_FORCE
        self.damping = MOVE_DAMPING
        self.textures = arcade.load_texture_pair(filename)

        self.health = HEALTH_FULL

        self.face = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

    def update_texture(self):
        self.texture = self.textures[self.face - 1]

    def dead(self):
        if self.health < HEALTH_EMPTY:
            self.health = HEALTH_EMPTY

        return self.health <= HEALTH_EMPTY

    def hurt(self, damage):
        self.health -= damage

        return self.dead()

    def update(self):
        if self.dead():
            return

        if self.health < HEALTH_FULL:
            self.health += HEALTH_REGENERATION_SPEED

        if self.health > HEALTH_FULL:
            self.health = HEALTH_FULL

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()

    def draw_overlay(self):
        window = arcade.get_window()

        if self.health >= HEALTH_FULL:
            return

        alpha = FULL_ALPHA - self.health * ONE_PERCENT_ALPHA

        arcade.draw_rectangle_filled(window.width / 2, window.height / 2,
                                     window.width, window.height,
                                     (255, 0, 0, alpha))

        if not self.dead():
            return

        # TODO: Implement real game over screen
        utils.text.create_text(
            _('Game Over'),
            width=window.width - (utils.text.MARGIN * 2),
            align='right').draw()
