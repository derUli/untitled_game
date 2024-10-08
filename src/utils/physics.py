""" Physics stuff """

import arcade
from arcade import PymunkPhysicsEngine, Scene

from constants.collisions import COLLISION_WALL, COLLISION_PLAYER, COLLISION_CAR, COLLISION_MOVEABLE, COLLISION_CRYSTAL
from constants.layers import (
    LAYER_MOVEABLE,
    LAYER_CAR_RIGHT,
    LAYER_CAR_LEFT,
    LAYER_WALL,
    LAYER_FENCE,
    LAYER_PIGGYBANK,
    LAYER_JEEP,
    LAYER_WATER,
    LAYER_TREE,
    LAYER_SKY,
    LAYER_RIVER,
    LAYER_ALPHA_WALL, LAYER_CRYSTAL
)
from sprites.characters.player import Player

DEFAULT_FRICTION = 1

DAMPING = 0.5
GRAVITY = (0, 0)


def make_physics_engine(player_sprite: Player, scene: Scene) -> PymunkPhysicsEngine:
    """
    Initializes a physics engine
    @param player_sprite: The player sprite
    @param scene: The scene
    @return: Pymunk Physics Engine
    """

    damping = DAMPING

    # Set the gravity. (0, 0) is good for outer space and top-down.
    gravity = GRAVITY

    physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

    # Add the player.
    # For the player, we set the damping to a lower value, which increases
    # the damping rate. This prevents the character from traveling too far
    # after the player lets off the movement keys.
    # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
    # rotating.
    # Friction normally goes between 0 (no friction) and 1.0 (high friction)
    # Friction is between two objects in contact. It is important to remember
    # in top-down games that friction moving along the 'floor' is controlled
    # by damping.
    physics_engine.add_sprite(
        player_sprite,
        friction=DEFAULT_FRICTION,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_PLAYER,
        damping=player_sprite.damping
    )

    # Create the walls.
    # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
    # move.
    # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
    # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
    # repositioned by code and don't respond to physics forces.
    # Dynamic is default.
    wall_layers = [
        LAYER_WALL,
        LAYER_FENCE,
        LAYER_PIGGYBANK,
        LAYER_TREE,
        LAYER_JEEP,
        LAYER_WATER,
        LAYER_SKY,
        LAYER_RIVER,
        LAYER_ALPHA_WALL,
    ]

    for layer in wall_layers:

        if layer not in scene.name_mapping:
            scene.add_sprite_list(layer)

        physics_engine.add_sprite_list(
            scene[layer],
            friction=0,
            collision_type=COLLISION_WALL,
            body_type=PymunkPhysicsEngine.STATIC
        )

    if LAYER_CRYSTAL not in scene.name_mapping:
        scene.add_sprite_list(LAYER_CRYSTAL)

    physics_engine.add_sprite_list(
        scene[LAYER_CRYSTAL],
        friction=0,
        collision_type=COLLISION_CRYSTAL,
        body_type=PymunkPhysicsEngine.STATIC
    )

    car_layers = [
        LAYER_CAR_LEFT,
        LAYER_CAR_RIGHT
    ]

    for layer in car_layers:
        if layer not in scene.name_mapping:
            scene.add_sprite_list(layer)

        physics_engine.add_sprite_list(
            scene[layer],
            mass=2,
            damping=0.01,
            collision_type=COLLISION_CAR,
            moment_of_intertia=arcade.PymunkPhysicsEngine.MOMENT_INF
        )

    # Create some boxes to push around.
    # Mass controls, well, the mass of an object. Defaults to 1.
    if LAYER_MOVEABLE in scene.name_mapping:
        physics_engine.add_sprite_list(
            scene[LAYER_MOVEABLE],
            collision_type=COLLISION_MOVEABLE,
            mass=2,
            damping=0.01,
        )

    return physics_engine


def on_hit_destroy(bullet_sprite, _hit_sprite, _arbiter, _space, _data):
    """
    On hit destroy handler for physics
    @param bullet_sprite: The bullet sprite
    @param _hit_sprite: The hit sprite
    @param _arbiter: TODO: What is this?
    @param _space: TODO: What is this?
    @param _data: TODO: What is this?
    """
    bullet_sprite.remove_from_sprite_lists()
