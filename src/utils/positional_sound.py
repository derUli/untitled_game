""" Positional sound """
import logging

import arcade

from utils.audio import normalize_volume

MAX_DISTANCE = 800
FADE_SPEED = 0.05


class PositionalSound:
    """ Positional sound """

    def __init__(self, listener, source, player, state):
        self.listener = listener
        self.source = source
        self.state = state
        self.player = player

        if self.player:
            self.player.volume = 0

    def update(self, init=False):
        if not self.player:
            return

        if not self.player.playing:
            return

        distance = arcade.get_distance_between_sprites(self.listener, self.source)
        distance = abs(distance)

        # Final volume = normalized sound volume × (max distance - distance) / max distance
        volume = self.player.volume

        if distance <= MAX_DISTANCE:
            volume = min(volume + FADE_SPEED, 1.0)
            if init:
                volume = 1.0
        else:
            volume = max(volume - FADE_SPEED, 0)
            if init:
                volume = 0.0

        volume = normalize_volume(volume * self.state.settings.sound_volume)

        if volume != self.player.volume:
            logging.debug('Sound volume at %s', volume)
            self.player.volume = volume

    def pause(self):
        if not self.player:
            return

        self.player.pause()

    def play(self):
        if not self.player:
            return

        self.update(init=True)
        self.player.play()

    @property
    def playing(self):
        if not self.player:
            return False

        return self.player.playing
