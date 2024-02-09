""" Cow character sprite """

import logging
import os
import random
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.killable import Killable
from sprites.maincharacter import PIG_SOUND_NOTHING
from sprites.weapon import Weapon
from utils.audio import play_sound, sounds_busy

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0

BLOOD_COLOR = (163, 8, 8)
SOUND_FADEOUT = 100


class Cow(Killable, Character):
    """ Cow sprite class """

    def __init__(self, sprite_dir, cache, sprite='cow.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sound = None
        self.next_direction_change = None
        # Time until next move
        self.walk_speed = random.randint(3, 5)

        self.next_sound_time = None

    def draw(self, screen, x, y):
        """ Draw sprite """
        if not self.next_sound_time and not sounds_busy():
            self.next_sound_time = time.time() + random.randint(10,  30)

            if time.time() >= self.next_sound_time:
                self.play_sound()

        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        return sprite, pos

    def random_direction(self):
        direction = random.choice([
            DIRECTION_LEFT,
            DIRECTION_RIGHT,
            DIRECTION_UP,
            DIRECTION_DOWN
        ])

        if direction == self.direction:
            return self.random_direction()

        return direction

    def calculate_next_direction_change(self):
        self.change_direction(self.random_direction())

        self.next_direction_change = time.time() + random.randint(5, 50)

        return self.next_direction_change

    def play_sound(self):
        if sounds_busy():
            return

        self.next_sound_time = time.time() + random.randint(10, 30)

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'cow')
        )

        files = [
            'cow1.ogg',
            'cow2.ogg',
            'cow3.ogg',
        ]
        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)

    def change_direction(self, direction):
        """ Change sprite direction """
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction

    def handle_interact_item(self, element):
        """ Handle interact """
        logging.debug('interact')
        # Destroy if player has the chainsaw
        if not element:
            return

        if self.killed():
            return

        if self.walkable:
            return

        # Chicken is killed by chainsaw
        if isinstance(element.state.inventory, Chainsaw):
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            self.start_fade()

            if self.sound and self.sound.get_busy():
                self.sound.fadeout(SOUND_FADEOUT)

            logging.debug('Cow killed by chainsaw')

            element.state.inventory.play_sound()

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )
        elif isinstance(element.state.inventory, Weapon):
            self.kill()
        else:
            element.play_sound(PIG_SOUND_NOTHING)

    def ai(self, level):
        if self.next_direction_change is None:
            self.calculate_next_direction_change()
            return

        if time.time() < self.last_movement + self.walk_speed:
            return

        if time.time() > self.next_direction_change:
            self.calculate_next_direction_change()

        self.walk_speed = random.randint(1, 3)

        z, y, x = level.search_sprite(self)

        next_x = x
        next_y = y

        if self.direction == DIRECTION_LEFT:
            next_x -= 1
        elif self.direction == DIRECTION_RIGHT:
            next_x += 1
        elif self.direction == DIRECTION_UP:
            next_y -= 1
        elif self.direction == DIRECTION_DOWN:
            next_y += 1

        walkable = level.is_walkable(next_x, next_y)

        if walkable:
            level.move_sprite(self, (z, next_y, next_x))
            self.last_movement = time.time()
        else:
            self.change_direction(self.random_direction())
