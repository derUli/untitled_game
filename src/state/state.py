import json
import os

from state.playerstate import PlayerState
from utils.image import ImageCache
from utils.reflections import get_class


class State:
    def __init__(self, data_dir=None):
        self.cache = ImageCache()
        self.sprites_dir = os.path.join(data_dir, 'images', 'sprites')
        """ Constructor """
        self.player_state = PlayerState(data_dir)
        self.level = 1
        self.edit_mode = False

    def to_dict(self):
        """ To dictionary """

        inventory = self.player_state.inventory
        if inventory:
            inventory = inventory.to_dict()

        return {
            'health': self.player_state.health,
            'inventory': inventory
        }

    def to_json(self):
        """ To json """
        return json.dumps(self.to_dict())

    def from_dict(self, savegame):
        """ From dictionary """
        self.player_state.health = savegame['health']
        self.player_state.update_health()
        self.player_state.inventory = None

        if 'inventory' in savegame and savegame['inventory']:
            inventory = savegame['inventory']

            if 'sprite_file' in inventory:
                sprite_file = inventory['sprite_file']
            klass = get_class(inventory['sprite_class'])
            self.player_state.inventory = klass(self.sprites_dir, self.cache, sprite_file)

    def from_json(self, data):
        """ To dictionary """
        savegame = json.loads(data)
        self.from_dict(savegame)
