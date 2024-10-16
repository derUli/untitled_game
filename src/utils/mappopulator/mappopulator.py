import logging
import random
import time

from arcade import SpriteList

from constants.layers import LAYER_SNOW
from sprites.characters.chicken import spawn_chicken
from sprites.decoration.hellparticle import HELL_PARTICLE_COLORS, HellParticle
from sprites.decoration.snow import Snow, SNOW_COLORS
from sprites.items.food import spawn_food
from sprites.items.landmine import spawn_landmine
from state.argscontainer import ArgsContainer
from utils.text import label_value


class MapPopulator:
    def __init__(self):
        """ Constructor """

        self.next_spawn = 0
        self.enabled = True

    def update(self, args: ArgsContainer) -> None:
        logging.error('MapPopulator update() not implemented')

    def spawn(self, args: ArgsContainer) -> None:
        if not self.enabled:
            return

        if not any(args.state.difficulty.spawn_what):
            return

        what = random.choice(args.state.difficulty.spawn_what)
        logging.info('Spawn ' + what)

        if what == 'Skull':
            self.spawn_skull(args)
        elif what == 'Slimer':
            self.spawn_slimer(args)
        elif what == 'Barrel':
            self.spawn_barrel(args)

        self.next_spawn = time.time() + random.randint(1, 6)

    def spawn_skull(self, args: ArgsContainer) -> None:
        """
        Spawn a skull
        
        @param: ArgsContainer
        """
        from sprites.characters.skull import spawn_skull
        spawn_skull(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_slimer(self, args: ArgsContainer) -> None:
        """
        Spawn a slimer

        @param: ArgsContainer
        """
        from sprites.characters.slimer import spawn_slimer
        spawn_slimer(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_barrel(self, args: ArgsContainer) -> None:
        """
        Spawn a slimer

        @param: ArgsContainer
        """
        from sprites.characters.barrel import spawn_barrel
        spawn_barrel(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_npcs(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        self.spawn_chicken(args)

    def spawn_initial(self, args: ArgsContainer) -> None:
        """ Spawn some sprites on level load """

        logging.error('MapPopulator spawn_initial() not implemented')

    def init_npc_spritelist(self, args):
        from constants.layers import LAYER_NPC
        args.scene.add_sprite_list(LAYER_NPC, SpriteList(lazy=True, use_spatial_hash=True))

    @staticmethod
    def spawn_landmine(args: ArgsContainer) -> None:

        if not args.state.difficulty.options['landmines']:
            return

        for i in range(random.randint(1, 4)):
            logging.info(f"Spawn landmine {i}")
            spawn_landmine(args.state, args.tilemap.map, args.scene, args.physics_engine)

    @staticmethod
    def spawn_chicken(args: ArgsContainer) -> None:
        if not args.state.difficulty.options['chicken']:
            return

        for i in range(random.randint(1, 3)):
            logging.info(f"Spawn chicken {i}")
            spawn_chicken(args.state, args.tilemap.map, args.scene, args.physics_engine)

    @staticmethod
    def spawn_food(args: ArgsContainer) -> None:
        for i in range(random.randint(1, 10)):
            spawn_food(args.state, args.tilemap.map, args.scene, args.physics_engine)

    def spawn_snow(self, args: ArgsContainer) -> None:
        if not args.state.difficulty.options['snow']:
            return

        if not args.state.settings.weather:
            return

        for i in range(1, 1000):
            snow = Snow(radius=8, color=random.choice(SNOW_COLORS), soft=True)
            snow.center_x = random.randint(0, args.tilemap.width)
            snow.center_y = random.randint(0, args.tilemap.height)

            args.scene.add_sprite(LAYER_SNOW, snow)

    def spawn_hell_particles(self, args: ArgsContainer) -> None:
        if not args.state.difficulty.options['hellParticles']:
            return

        if not args.state.settings.weather:
            return

        for i in range(1, 500):
            radius = random.randint(1, 14)
            particle = HellParticle(radius=radius, color=random.choice(HELL_PARTICLE_COLORS), soft=True)
            particle.center_x = random.randint(0, args.tilemap.width)
            particle.center_y = random.randint(0, args.tilemap.height)

            args.scene.add_sprite(LAYER_SNOW, particle)


def init_map_populator(gamemode: str) -> MapPopulator:
    from constants.gamemode import GAMEMODE_CAMPAIGN

    if gamemode == GAMEMODE_CAMPAIGN:
        from utils.mappopulator.campaignmappopulator import CampaignMapPopulator
        return CampaignMapPopulator()
    else:
        gamemode = 'Unknown'

    logging.error(label_value('MapPopulator', gamemode))
