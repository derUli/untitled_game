""" Main character sprite """

import logging

import pygame

from constants.graphics import SPRITE_SIZE
from constants.headup import NPC_HEALTH_COLOR_FRIENDLY, NPC_HEALTH_HEIGHT
from sprites.blood import Blood
from sprites.character import Character
from utils.atmosphere import ATMOSPHERE_FOG

HORSE_FOG = 255

TASK_ID = 'horse'


class Horse(Character):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='horse.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sentence = -1
        self.attributes = {
            'blood': 0,
            'given_blood': 0
        }

        self.task = None

        self.sentences = [
            _('Infinity bloodless!'),
            _('I don\'t have a single drop of blood left.'),
            _('Please give me some blood!'),
            _('I am infinitely thirsty for blood.')
        ]

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        pos = self.calculate_pos(x, y)

        self.draw_health(screen, pos)

    def draw_health(self, screen, pos):

        x, y = pos
        w, h = SPRITE_SIZE

        y += h - NPC_HEALTH_HEIGHT

        w = w / 100 * self.attributes['blood']
        h = NPC_HEALTH_HEIGHT

        surface = pygame.surface.Surface((w, h))

        surface.fill(NPC_HEALTH_COLOR_FRIENDLY)

        screen.blit(surface, (x, y))

    def next_sentence(self):
        self.sentence += 1

        if self.sentence >= len(self.sentences):
            self.sentence = 0

        return self.sentences[self.sentence]

    def handle_interact(self, element):
        if element and element.state:
            if element.state.display_text.is_visible():
                return

            element.state.say(self.next_sentence())

            self.task = TASK_ID

    def ai(self, level):
        part = 0.5

        if round(self.attributes['given_blood']) <= 0:
            return

        self.attributes['blood'] += part
        self.attributes['given_blood'] -= part

        if self.attributes['blood'] > 100:
            self.attributes['blood'] = 100
            self.attributes['given_blood'] = 0

        if self.attributes['blood'] < 0:
            self.attributes['blood'] = 0

    def handle_interact_item(self, element):
        """ Handle interact """
        logging.debug('interact')
        if not element:
            return

        if isinstance(element.state.inventory, Blood):
            amount = element.state.inventory.blood_amount

            element.state.inventory.blood_amount -= amount
            self.attributes['given_blood'] += amount

            element.state.inventory = None
            self.sentences = [
                _('Now I have a bit more blood.'),
                _('I still haven\'t enough blood.'),
                _('Yummy blood!'),
                _('Give me more blood!'),
                _('Tasty blood!'),
                _('I need more blood!')
            ]
            self.sentence = -1

            element.state.say(self.next_sentence())

    def update_atmosphere(self, atmosphere):
        fog = atmosphere.get_layer_by_id(ATMOSPHERE_FOG)

        if not fog:
            return

        if self.attributes['blood'] >= 100:
            fog.update(0)
            return

        fog.update(HORSE_FOG)

    def update_state(self, state):
        if self.task:
            state.task.set_task_id(self.task)
            self.task = None
