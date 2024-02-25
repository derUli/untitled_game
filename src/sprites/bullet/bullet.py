import arcade
from arcade import FACE_RIGHT, FACE_LEFT

import views.gameview
from sprites.characters.enemysprite import EnemySprite

HURT = 10

MASS = 0.1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1

FORCE_MOVE = 2000


class Bullet(arcade.sprite.SpriteCircle):
    def __init__(
            self,
            radius,
            color=arcade.csscolor.BLACK,
            soft=False,
            force_move=FORCE_MOVE,
            hurt=HURT
    ):
        super().__init__(radius, color=color, soft=soft)

        self.force_move = force_move
        self.hurt = hurt

    def draw_debug(self):
        pass

    def draw_overlay(self):
        pass

    def setup(self, source, physics_engine, scene, state):

        self.center_y = source.center_y

        if source.face == FACE_RIGHT:
            self.right = source.right + self.width
        elif source.face == FACE_LEFT:
            self.force_move = -self.force_move
            self.left = source.left - self.width

        scene.add_sprite(views.gameview.SPRITE_LIST_ENEMIES, self)

        state.play_sound('shot')

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="bullet",
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler('bullet', 'wall', post_handler=self.on_hit)
        physics_engine.add_collision_handler('bullet', 'enemy', post_handler=self.on_hit)

        physics_engine.apply_force(self, (self.force_move, 0))

    def on_hit(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()

        if isinstance(_hit_sprite, EnemySprite):
            _hit_sprite.hurt(10)
