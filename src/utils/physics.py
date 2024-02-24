from arcade import PymunkPhysicsEngine

DEFAULT_FRICTION = 1

# Gravity
GRAVITY = (0, 0)


def make_physics_engine(player_sprite, scene):
    damping = 0.5

    # Set the gravity. (0, 0) is good for outer space and top-down.
    gravity = GRAVITY

    physics_engine = PymunkPhysicsEngine(damping=damping,
                                         gravity=gravity)

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
    physics_engine.add_sprite(player_sprite,
                              friction=DEFAULT_FRICTION,
                              moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                              collision_type="player",
                              max_velocity=400,
                              damping=player_sprite.damping,
                              )

    # Create the walls.
    # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
    # move.
    # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
    # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
    # repositioned by code and don't respond to physics forces.
    # Dynamic is default.
    physics_engine.add_sprite_list(scene['Walls'],
                                   friction=DEFAULT_FRICTION,
                                   collision_type="wall",
                                   body_type=PymunkPhysicsEngine.STATIC
                                   )

    # Create some boxes to push around.
    # Mass controls, well, the mass of an object. Defaults to 1.
    physics_engine.add_sprite_list(scene['Moveable'],
                                   mass=2,
                                   collision_type="rock"
                                   )

    return physics_engine