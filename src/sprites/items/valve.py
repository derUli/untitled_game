from sprites.items.item import Item, Interactable
from sprites.items.valvetarget import ValveTarget

class Valve(Item):

    def on_use_with(self, b, args):
        from constants.layers import LAYER_VALVE_TARGET
        if isinstance(b, ValveTarget):
            placed_valve = PlacedValve(self.filename, center_x = self.center_x, center_y = self.center_y)
            placed_valve.position = args.scene[LAYER_VALVE_TARGET][0].position
            args.scene[LAYER_VALVE_TARGET].clear()
            args.scene[LAYER_VALVE_TARGET].append(placed_valve)

            selected, index = args.inventory.get_selected()
            if selected.pop() == 0:
                args.player.set_item(None)


class PlacedValve(Interactable):
    def on_interact(self, args):

        from constants.layers import LAYER_RIVER

        if not any(args.scene[LAYER_RIVER]):
            args.state.noaction()
            return

        args.state.play_sound('valve')
        self.turn_right()

        alpha = None

        for water in args.scene[LAYER_RIVER]:
            if alpha is None:
                alpha = water.alpha - 50

            if alpha <= 0:
                alpha = 0

            water.alpha = alpha

        if alpha <= 0:
            for water in args.scene[LAYER_RIVER]:
                water.remove_from_sprite_lists()

        # TODO:
        # args.state.noaction()

    def copy(self):
        """ Copy item """
        return Valve(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )