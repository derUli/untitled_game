""" Slimer sprite class """
import os

import arcade
from arcade import FACE_RIGHT

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_NPC, check_collision_with_layers, WALL_LAYERS, LAYER_MOVEABLE
from sprites.characters.character import Character
from utils.sprite import random_position

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MASS = 0.05
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 300

SIGHT_DISTANCE = 1400
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4


class Barrel(Character):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(filename, center_x, center_y)

        self.fade_in = True
        self.explosion = None

        if self.fade_in:
            self.alpha = 0

    def draw_overlay(self, args):
        if self.explosion:
            return

        if self._health < 100:
            self.draw_healthbar()

    def update(
            self,
            delta_time,
            args
    ):
        if self.explosion:
            self.update_explosion(delta_time, args)
            return

        if self.dead:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

            return

        if self.fade_in and self.alpha < FADE_IN_MAX:
            new_alpha = self.alpha + FADE_SPEED

            if new_alpha >= FADE_IN_MAX:
                new_alpha = FADE_IN_MAX
                self.fade_in = False

            self.alpha = new_alpha

            return

        if args.player.center_y > self.center_y:
            return

        args.physics_engine.apply_force(self, (0, -FORCE_MOVE))

        explodes = False

        if arcade.check_for_collision(self, args.player):
            explodes = True

        layers = WALL_LAYERS + [LAYER_MOVEABLE, LAYER_NPC]

        for layer in layers:
            if not layer in args.scene.name_mapping:
                break

            collisions = arcade.check_for_collision_with_list(self, args.scene[layer])
            for collision in collisions:
                if collision != self:
                    explodes = True
                    break

        if explodes:
            # TODO: Explosion
            self.spawn_explosion(args)

    def update_explosion(self, delta_time, args):
        self.explosion_hurt(args)

        self.explosion.update_animation(delta_time)

        if self.explosion.cur_frame_idx >= len(self.explosion.frames) - 1:
            self.explosion.remove_from_sprite_lists()
            self.remove_from_sprite_lists()
        return

    def explosion_hurt(self, args):

        hurt = 30

        if arcade.get_distance_between_sprites(self.explosion, args.player) < 300:
            args.player.hurt(hurt)

        npcs = arcade.check_for_collision_with_list(self.explosion, args.scene[LAYER_NPC])

        for sprite in npcs:
            if isinstance(sprite, Character) and sprite != self:
                sprite.hurt(hurt)

    def spawn_explosion(self, args):
        gif = arcade.load_animated_gif(os.path.join(args.state.animation_dir, 'explosion.gif'))
        gif.position = self.position
        self.explosion = gif

        args.scene.add_sprite(LAYER_NPC, gif)
        self.explosion.sound = args.state.play_sound('explosion')

        self.alpha = 0

def spawn_barrel(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    barrel = Barrel(
        filename=os.path.join(
            state.sprite_dir,
            'monster',
            'barrel',
            'barrel.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if check_collision_with_layers(scene, barrel):
        return spawn_barrel(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_NPC, barrel)
    physics_engine.add_sprite(
        barrel,
        friction=FRICTION,
        collision_type=COLLISION_ENEMY,
        mass=MASS,
        elasticity=ELASTICITY,
        damping=DAMPING
    )