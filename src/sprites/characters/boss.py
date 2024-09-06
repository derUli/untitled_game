""" Slimer sprite class """
import os
import random

import PIL
import arcade
import pyglet.clock
from arcade import FACE_RIGHT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY
from sprites.characters.character import Character
from window.gamewindow import UPDATE_RATE

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MASS = 0.1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 200000

SIGHT_DISTANCE = 1400
COLLISION_CHECK_DISTANCE = 200
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4

EYE_OFFSET_X = 100
EYE_SPACING_X = 250
EYE_OFFSET_Y = 10

ALPHA_SPEED = 4
ALPHA_MAX = 255

class Boss(Character):
    def __init__(
            self,
            filename: str | None = None,
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
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.eye_file = os.path.join(os.path.dirname(filename), 'eye.png')
        self.laser_file = os.path.join(os.path.dirname(filename), 'laser.jpg')
        self.eye1 = None
        self.eye2 = None
        self.spawn_sound = None
        self.triggered = False
        self.lasers = []
        self.fighting = False
        self.force = random.choice([FORCE_MOVE, FORCE_MOVE * -1])

        self._should_shoot = False

    def update(self, delta_time, args):

        super().update(delta_time, args)

        self.eye1.center_x = self.center_x - EYE_OFFSET_X
        self.eye1.center_y = self.center_y - EYE_OFFSET_Y
        self.eye1.alpha = self.alpha

        self.eye2.center_x = self.eye1.center_x + EYE_SPACING_X
        self.eye2.center_y = self.eye1.center_y
        self.eye2.alpha = self.alpha

        if self.dead:
            self.unschedule()
            for laser in self.lasers:
                laser.remove_from_sprite_lists()

            # Fade out on death
            self.fade_destroy()

            # Complete level after boss killed
            if self.alpha <= 0:
                args.callbacks.on_complete()

            return

        w, h = arcade.get_window().get_size()
        if not self.triggered and arcade.get_distance_between_sprites(self, args.player) < h:
            self.triggered = True

            self.spawn_sound = args.state.play_sound('boss', 'spawn')
            return

        if not self.triggered:
            return

        if self.alpha < ALPHA_MAX:
            alpha = self.alpha + ALPHA_SPEED

            if alpha > ALPHA_MAX:
                alpha = ALPHA_MAX

            self.alpha = alpha

        if not self.spawn_sound.playing and not self.fighting:
            self.fighting = True
            pyglet.clock.schedule_interval_soft(self.should_shoot, 1 / 4, args)
            pyglet.clock.schedule_interval_soft(self.collision_lasers, 1 / 72, args)


        if not self.fighting:
            return

        if self.force > 0 and self.center_y > 2700:
            self.force *= -1
        elif self.force < 0 and self.center_y < 520:
            self.force *= -1

        args.physics_engine.apply_force(self, (0, self.force))

        self.update_laser(args)

    def update_laser(self, args):
        if not self._should_shoot:
            return

        laser_index = 0

        i = 0
        for laser in self.lasers:

            if laser.visible:
                laser_index = i
                break
            i += 1

        self.lasers[laser_index].visible = False

        if laser_index + 1 < len(self.lasers):
            next_laser = self.lasers[laser_index + 1]
            next_laser.visible = True
            if args.player.left > self.right:
                next_laser.left = self.eye2.right
            else:
                next_laser.right = self.eye1.left

            next_laser.center_y = self.eye1.center_y
        else:
            self.lasers[laser_index].visible = False
            self.lasers[0].visible = True
            self._should_shoot = False

    def setup(self, args):
        self.setup_boss(args)
        self.setup_eyes(args)
        self.setup_laser(args)

    def setup_boss(self, args):

        self.alpha = 0
        from constants.layers import LAYER_NPC

        self.remove_from_sprite_lists()

        args.scene.add_sprite(LAYER_NPC, self)

        args.physics_engine.add_sprite(
            self,
            mass=500,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            collision_type=COLLISION_ENEMY
        )

    def setup_eyes(self, args):
        from constants.layers import LAYER_NPC

        self.eye1 = arcade.sprite.Sprite(filename=self.eye_file)
        args.scene.add_sprite(LAYER_NPC, self.eye1)

        self.eye2 = arcade.sprite.Sprite(filename=self.eye_file, flipped_horizontally=True)
        args.scene.add_sprite(LAYER_NPC, self.eye2)

    def collision_lasers(self, delta_time, args):

        visible = list(filter(lambda x: x.visible, self.lasers))

        if not any(visible):
            return

        if arcade.check_for_collision(visible[0], args.player):
            args.player.hurt(args.state.difficulty.boss_laser_hurt)


    def setup_laser(self, args):
        from constants.layers import LAYER_NPC

        self.lasers = []


        laser_image = PIL.Image.open(
            self.laser_file
        ).convert('RGBA')

        laser_image = laser_image.resize((laser_image.width * 3, laser_image.height * 2))

        laser_range = []

        for i in range(1, int(UPDATE_RATE * laser_image.width)):
            laser_range.append(i * 72)


        for i in laser_range:
            image = laser_image.crop((0, 0, i, laser_image.height))
            texture = arcade.texture.Texture(image=image, name=f"laser-{i}")
            sprite = arcade.sprite.Sprite(texture=texture)
            sprite.visible = False
            self.lasers.append(sprite)
            args.scene.add_sprite(LAYER_NPC, sprite)

    def draw_overlay(self, args):
        self.draw_healthbar()


    def should_shoot(self, delta_time, args):
        if self._should_shoot:
            return

        w, h = arcade.get_window().get_size()

        if arcade.get_distance_between_sprites(self, args.player) < h:
            self._should_shoot = True
            self.lasers[0].visible = True

    def unschedule(self):
        pyglet.clock.unschedule(self.should_shoot)
        pyglet.clock.unschedule(self.collision_lasers)