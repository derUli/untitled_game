""" Sprite utilities """

import random

import arcade
from arcade import TileMap

from constants.layers import LAYER_WATER
from utils.scene import get_layer


def tilemap_size(tilemap: TileMap) -> tuple:
    """
    Calculate pixel size of a tilemap
    @param tilemap: The tile map
    @return: (width, height)
    """
    width = tilemap.width * tilemap.tile_width
    height = tilemap.height * tilemap.tile_height
    return width, height


def random_position(tilemap: TileMap) -> tuple:
    """
    Get a random position on a tilemap
    @param tilemap: The tile map
    @return: (x, y)
    """
    width, height = tilemap_size(tilemap)

    rand_x = random.randint(0, width)
    rand_y = random.randint(0, height)

    return rand_x, rand_y

def animated_in_sight(scene, player_sprite):

    layers = [LAYER_WATER]

    animated = []

    for name in layers:
        layer = get_layer(name, scene)
        for sprite in layer:
            w, h = arcade.get_window().get_size()
            diff = abs(arcade.get_distance_between_sprites(player_sprite, sprite))
            if diff <= h:
                animated.append(sprite)

    return animated

