from sprites.items.item import Item
from sprites.items.jeep import Jeep
from utils.callbackhandler import CallbackHandler


class CarKey(Item):
    def on_use_with(self, b, state=None, handlers: CallbackHandler | None = None):
        if isinstance(b, Jeep):
            state.play_sound('car', 'start')
            handlers.on_complete()
            return

        state.beep()
