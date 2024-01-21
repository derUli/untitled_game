""" Backdrop sprite """

import math
import time

from PygameShader.shader import wave

import sprites.sprite
from utils.quality import shader_enabled

LAVA_SPEED = 2

DAMAGE_AMOUNT = 33

class Lava(sprites.sprite.Sprite):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite='lava.jpg'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.walkable = False
        self.player_state = None
        self.original_sprite = self.sprite.copy().convert()

        self.angle = 0
        self.loaded = False
        self.player_State = None
        self.update_interval = (1 / 10)
        self.last_update = 0

    def draw(self, screen, x, y):
        pos = self.calculate_pos(x, y)

        if not shader_enabled():
            super().draw(screen, x, y)
            return

        if not self.loaded:
            self.generate_frames()

        frame = self.cache.get_processed_image(self.cache_id(self.angle))

        if not frame:
            return

        screen.blit(frame, pos)

        if time.time() - self.last_update < self.update_interval:
            return

        next_angle = self.angle + LAVA_SPEED
        next_angle = next_angle % 360

        if self.cache.get_processed_image(self.cache_id(next_angle)):
            self.last_update = time.time()
            self.angle = next_angle

    def generate_frames(self):
        self.loaded = True

        angle = 0
        while angle <= 360:
            if not self.cache.get_processed_image(self.cache_id(angle)):
                self.cache.add_processed_image(
                    self.cache_id(angle), self.next_frame(angle))

            angle += LAVA_SPEED

    def preload(self):
        self.generate_frames()

    def cache_id(self, angle):
        return 'lava-' + str(angle)

    def next_frame(self, angle):
        sprite = self.original_sprite.copy()

        # w, h = sprite.get_size()

        wave(sprite, angle * math.pi / 180.0, 12)
        # sprite = scale_method()(sprite, (w + 90, h + 90))

        sprite = sprite.convert()

        return sprite

    def handle_interact(self, element):
        if element and element.state:
            element.state.hurt(DAMAGE_AMOUNT)
