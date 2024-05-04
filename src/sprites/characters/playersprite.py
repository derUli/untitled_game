""" Player sprite class """
import random

import arcade
from arcade import FACE_RIGHT, FACE_LEFT, FACE_DOWN, FACE_UP

import utils.text
from constants.layers import LAYER_SPAWN_POINT, LAYER_PLAYER
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, SpriteHealth

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 1500

MODIFIER_DEFAULT = 1
MODIFIER_SPRINT = 1.5

MOVE_DAMPING = 0.01

HEALTH_REGENERATION_SPEED = 0.1

FULL_ALPHA = 255
ONE_PERCENT_ALPHA = FULL_ALPHA / 100

PLACE_ITEM_ALPHA = 100

INVENTORY_MARGIN = 15

SPAWN_POINT = (0, 0)


class PlayerSprite(Character, SpriteHealth):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        self.move_force = MOVE_FORCE
        self.modifier = MODIFIER_DEFAULT
        self.damping = MOVE_DAMPING
        self.textures = arcade.load_texture_pair(filename)

        self.health = HEALTH_FULL
        self.textures = arcade.load_texture_pair(filename)
        self.face = DEFAULT_FACE
        self.face_horizontal = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

        self.scale = 0.9
        self.item = None
        self._died = False

        self.state = None
        self.gameover_text = None
        self.gameover_text_rendered = None
        self.water = False

        self.footsteps_default = None
        self.footsteps_sprint = None

    def setup(self, state, scene, callbacks):
        self.state = state
        self.scene = scene
        self.callbacks = callbacks

        self.center_x, self.center_y = SPAWN_POINT

        if LAYER_SPAWN_POINT not in self.scene.name_mapping:
            return

        for sprite in self.scene.get_sprite_list(LAYER_SPAWN_POINT):
            self.center_x, self.center_y = sprite.center_x, sprite.center_y
            sprite.remove_from_sprite_lists()

        sausages = [
            _('bacon'),
            _('salami'),
            _('schnitzel'),
            _('Cutlet'),
            _('Mett'),
            _('Suckling pig'),
            _('Pulled Pork'),
            _('Spare ribs')
        ]

        self.gameover_text = _('You are') + ' ' + random.choice(sausages) + '!'

        scene.add_sprite(LAYER_PLAYER, self)

        self.footsteps_default = state.play_sound('footsteps', loop=True, speed=MODIFIER_DEFAULT)
        self.footsteps_default.pause()

        self.footsteps_sprint = state.play_sound('footsteps', loop=True, speed=MODIFIER_SPRINT)
        self.footsteps_sprint.pause()

    def update_texture(self):
        self.texture = self.textures[self.face_horizontal - 1]

    def reset(self):
        self.modifier = MODIFIER_DEFAULT

    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        if self.dead:
            return

        if self.health < HEALTH_FULL:
            self.health += HEALTH_REGENERATION_SPEED

        if self.health > HEALTH_FULL:
            self.health = HEALTH_FULL

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.set_face(FACE_LEFT)
        elif self.change_x > 0:
            self.set_face(FACE_RIGHT)
        elif self.change_y > 0:
            self.set_face(FACE_DOWN)
        elif self.change_y < 0:
            self.set_face(FACE_UP)

        if self.item:
            self.item.alpha = PLACE_ITEM_ALPHA
            if self.face == FACE_RIGHT:
                self.item.left = self.right + INVENTORY_MARGIN
                self.item.center_y = self.center_y
            elif self.face == FACE_LEFT:
                self.item.right = self.left - INVENTORY_MARGIN
                self.item.center_y = self.center_y
            elif self.face == FACE_UP:
                self.item.center_x = self.center_x
                bottom = self.top + INVENTORY_MARGIN

                if self.item.height > self.item.width:
                    bottom += INVENTORY_MARGIN

                self.item.bottom = bottom

            elif self.face == FACE_DOWN:
                self.item.center_x = self.center_x
                top = self.bottom - INVENTORY_MARGIN

                if self.item.height > self.item.width:
                    top -= INVENTORY_MARGIN

                self.item.top = top

            self.item.draw_item(self.face)

    def draw_overlay(self):
        window = arcade.get_window()

        if self.health >= HEALTH_FULL:
            return

        alpha = FULL_ALPHA - self.health * ONE_PERCENT_ALPHA

        arcade.draw_rectangle_filled(window.width / 2, window.height / 2,
                                     window.width, window.height,
                                     (255, 0, 0, alpha))

        if not self.dead:
            return

        if not self.gameover_text_rendered:
            self.gameover_text_rendered = utils.text.create_text(
                self.gameover_text,
                width=window.width - (utils.text.MARGIN * 2),
                align='left')

        self.gameover_text_rendered.draw()

    def set_item(self, item):
        if self.item:
            self.item.alpha = 255

            if item is None:
                self.item.remove_from_sprite_lists()

        self.item = item
        return item

    def get_item(self):
        return self.item

    def set_face(self, face):
        if face in [FACE_LEFT, FACE_RIGHT]:
            self.face_horizontal = face
            self.update_texture()

        self.face = face

    def on_die(self) -> None:
        """ Called when the player dies """
        self.state.squeak()

    def start_walk(self, sprint=False):
        volume = 1
        self.footsteps_default.volume = volume * self.state.settings.sound_volume
        self.footsteps_sprint.volume = volume * self.state.settings.sound_volume

        if sprint:

            if self.footsteps_default.playing:
                self.footsteps_default.pause()

            if not self.footsteps_sprint.playing:
                self.footsteps_sprint.play()
                return

        if self.footsteps_sprint.playing:
            self.footsteps_sprint.pause()

        if not self.footsteps_default.playing:
            self.footsteps_default.play()

    def stop_walk(self):
        self.footsteps_default.pause()

    @property
    def sprinting(self):
        return self.modifier == MODIFIER_SPRINT
