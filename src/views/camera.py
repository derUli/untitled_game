def center_camera_to_player(player_sprite, camera):
    # Find where player is, then calculate lower left corner from that
    screen_center_x = player_sprite.center_x - (camera.viewport_width / 2)
    screen_center_y = player_sprite.center_y - (camera.viewport_height / 2)

    # Set some limits on how far we scroll
    if screen_center_x < 0:
        screen_center_x = 0
    if screen_center_y < 0:
        screen_center_y = 0

    # Here's our center, move to it
    player_centered = screen_center_x, screen_center_y
    camera.move_to(player_centered)
