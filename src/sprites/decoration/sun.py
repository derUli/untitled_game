""" Sun """
from arcade import Scene, Camera

from sprites.sprite import Sprite
from utils.scene import get_layer

MARGIN_RIGHT = 20


class Sun(Sprite):
    """ Sun """

    def update(self, delta_time, args):
        """ Update sun position """
        camera_x, camera_y = args.camera.position
        x, y, viewport_w, viewport_h = args.camera.viewport

        self.left = camera_x + viewport_w - self.width - MARGIN_RIGHT

