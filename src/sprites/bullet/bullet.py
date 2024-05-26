""" Pig bullet """
import arcade
import logging
import math
import time
from arcade import FACE_RIGHT, FACE_LEFT

from constants.collisions import COLLISION_ENEMY, COLLISION_BULLET, COLLISION_WALL, COLLISION_CHICKEN, \
    COLLISION_MOVEABLE
from constants.layers import LAYER_NPC
from sprites.characters.character import Character
from sprites.characters.chicken import Chicken
from sprites.sprite import AbstractSprite
from utils.physics import on_hit_destroy

HURT_DEFAULT = 20
HURT_CHICKEN = 35

MASS = 0.05
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 3800

# Destroy after X seconds
DESTROY_TIME = 2

SCORE_HURT_CHICKEN = 25
SCORE_HURT_SKULL = 50


class Bullet(AbstractSprite, arcade.sprite.SpriteCircle):
    def __init__(
            self,
            radius,
            color=arcade.csscolor.BLACK,
            soft=False,
            force_move=FORCE_MOVE,
            hurt=HURT_DEFAULT,
            hurt_modifier=1.0
    ):
        super().__init__(radius, color=color, soft=soft)

        self.force_move = force_move
        self.hurt = hurt
        self.hurt_modifier = hurt_modifier
        self.created_at = time.time()
        self.state = None

    def update(
            self,
            delta_time,
            args
    ):
        if time.time() >= self.created_at + DESTROY_TIME:
            logging.debug('Remove bullet from scene')
            self.remove_from_sprite_lists()

    def setup(self, source, physics_engine, scene, state):

        self.state = state
        self.center_y = source.center_y

        if source.face_horizontal == FACE_RIGHT:
            self.right = source.right + self.width
        elif source.face_horizontal == FACE_LEFT:
            self.force_move = -self.force_move
            self.left = source.left - self.width

        state.play_sound('shot')

        scene.add_sprite(LAYER_NPC, self)
        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="bullet",
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_WALL, post_handler=on_hit_destroy)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_BULLET, post_handler=on_hit_destroy)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_ENEMY, post_handler=self.on_hit)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_CHICKEN, post_handler=self.on_hit)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_MOVEABLE, post_handler=self.on_hit)

        physics_engine.apply_force(self, (self.force_move, 0))

        return self

    def on_hit(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()

        if not isinstance(_hit_sprite, Character):
            return

        hurt = self.hurt

        score = SCORE_HURT_SKULL

        if isinstance(_hit_sprite, Chicken):
            hurt = HURT_CHICKEN
            score = SCORE_HURT_CHICKEN

        hurt = hurt * self.hurt_modifier

        self.state.score += math.floor(self.hurt_modifier * score)

        _hit_sprite.hurt(hurt)
