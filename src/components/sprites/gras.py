import constants.graphics
import components.sprites.sprite
import pygame

class Gras(components.sprites.sprite.Sprite):
    def __init__(self, sprite_dir, sprite = None):
        super().__init__(sprite_dir, 'gras.jpg')
        