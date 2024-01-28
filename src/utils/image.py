import logging
import os.path
import time
from typing import Union

import pygame
from PygameShader import bilinear

from constants.graphics import ALPHA_IMAGE_FORMATS
from utils.quality import scale_method


class ImageCache:

    def __init__(self):
        self.images = {}
        self.processed_images = {}

    def clear(self):
        self.images = {}
        self.processed_images = {}

    def add_processed_image(self, name: str,
                            surface: pygame.surface.Surface) -> None:
        self.processed_images[name] = surface

    def get_processed_image(self, name: str) -> pygame.surface.Surface:
        if name in self.processed_images:
            return self.processed_images[name]

        return None

    def load_image(self, path: str, scale: Union[tuple, None] = None) -> Union[pygame.surface.Surface, None]:
        time.time()
        extension = os.path.splitext(path)[1]
        is_alpha = extension.lower() in ALPHA_IMAGE_FORMATS

        scale_fn = scale_method()

        cache_id = path
        if scale:
            x, y = scale

            cache_id = cache_id + '-' + str(x) + '-' + str(y)

        if cache_id not in self.images:
            try:
                image = pygame.image.load(path)

                if is_alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()

                is_smoothscale = scale_fn == pygame.transform.smoothscale
                is_scaledown = scale and scale < image.get_size()

                # bilinear is much faster than smoothscale for scaling down
                # But it is slower for scaling up and has no alpha support
                if is_smoothscale and is_scaledown and not is_alpha:
                    scale_fn = bilinear

                if scale and image.get_size() != scale:
                    image = scale_fn(image, scale)

                self.images[cache_id] = image

            except FileNotFoundError:
                logging.error(' '.join(['File not found', path]))
                self.images[cache_id] = None

        return self.images[cache_id]
