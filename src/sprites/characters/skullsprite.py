""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from utils.physics import DEFAULT_FRICTION

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
PLAYER_MOVE_FORCE = 1000
PLAYER_DAMPING = 0.2

SIGHT_DISTANCE = 500
SIGHT_CHECK_RESOLUTION = 2


class SkullSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(center_x=center_x, center_y=center_y)

        self.move_force = PLAYER_MOVE_FORCE
        self.damping = PLAYER_DAMPING

        dirname = os.path.join(os.path.dirname(filename))

        self.skull_off = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull.png')
        )
        self.skull_on = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull2.png')
        )

        self.chasing = False

        self.friction = DEFAULT_FRICTION

        self.face = DEFAULT_FACE
        self.textures = None
        self.astar_barrier_list = None
        self.update_texture()

    def update_texture(self):
        if self.chasing:
            self.textures = self.skull_on
        else:
            self.textures = self.skull_off

        self.texture = self.textures[self.face - 1]

    def update(self, player=None, walls=None):

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()

        if not player or not walls:
            return

        grid_size = self.texture.width * self._scale

        # Calculate the playing field size. We can't generate paths outside of
        # this.
        playing_field_left_boundary = -grid_size * 2
        playing_field_right_boundary = grid_size * 35
        playing_field_top_boundary = grid_size * 17
        playing_field_bottom_boundary = -grid_size * 2
        self.update_texture()

        if arcade.has_line_of_sight(player.position,
                                 self.position,
                                 walls=walls,
                                 check_resolution=SIGHT_CHECK_RESOLUTION,
                                 max_distance=SIGHT_DISTANCE
                                 ):
            self.chasing = player

        if self.chasing:
            if not self.astar_barrier_list:
                self.astar_barrier_list = arcade.AStarBarrierList(
                    moving_sprite=self,
                    blocking_sprites=walls,
                    grid_size=grid_size,
                    left=int(playing_field_left_boundary),
                    right=playing_field_right_boundary,
                    bottom=int(playing_field_bottom_boundary),
                    top=playing_field_top_boundary
                )

            arcade.astar_calculate_path(self.position,
                                              player.position,
                                              self.astar_barrier_list,
                                              diagonal_movement=False)

