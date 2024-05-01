import random

from sprites.items.item import Item, Tree


class Chainsaw(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.ferret import Ferret
        from sprites.characters.skullsprite import SkullSprite

        if isinstance(b, Tree):
            b.fade_destroy()
            # TODO: Chainsaw sound
            sound_number = random.randint(1, 4)
            state.play_sound('chainsaw' + str(sound_number))
            return

        if isinstance(b, SkullSprite):
            b.hurt(50)
            return

        if isinstance(b, Ferret):
            b.hurt(100)
            return

        state.beep()
