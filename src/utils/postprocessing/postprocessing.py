import os

import arcade

from utils.postprocessing.colortint import ColorTint
from utils.postprocessing.filmgrain import FilmGrain
from utils.postprocessing.fog import Fog
from utils.sprite import load_animated_gif


class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args):
        self.pipeline = []

        if args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        self.pipeline.append(
            ColorTint().setup(args)
        )
        self.pipeline.append(
            FilmGrain().setup(args)
        )

        return self

    def update(self, delta_time, args) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()