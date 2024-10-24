""" Settings > Audio """
import logging

import arcade.gui
from arcade.gui.widgets.slider import UISlider

import constants.controls.keyboard
import utils.gui
import utils.text
from constants.gui import BUTTON_WIDTH
from views.fading import Fading

COLOR_BACKGROUND = (123, 84, 148)


class SettingsAudio(Fading):
    """ Settings > Audio """

    def __init__(self, window, state, previous_view, shadertoy, time=0):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = shadertoy
        self.time = time

        self.previous_view = previous_view
        self._fade_in = None

        self.background = COLOR_BACKGROUND

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """

        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self) -> None:
        """ Disable the UIManager when the view is hidden. """

        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

    def setup(self) -> None:
        """ Setup the audio settings screen """

        self.manager.clear()
        self.manager.disable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        master_label = arcade.gui.UILabel(
            text=_('Master Volume'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        master_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._master_volume * 100),
            min_value=0,
            max_value=100,
            style=utils.gui.get_slider_style()
        )

        music_label = arcade.gui.UILabel(
            text=_('Music'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        music_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._music_volume * 100),
            min_value=0,
            max_value=100,
            style=utils.gui.get_slider_style()
        )

        sound_label = arcade.gui.UILabel(
            text=_('Sound'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        sound_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._sound_volume * 100),
            min_value=0,
            max_value=100,
            style=utils.gui.get_slider_style()
        )

        atmo_label = arcade.gui.UILabel(
            text=_('Environment'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        atmo_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._atmo_volume * 100),
            min_value=0,
            max_value=100,
            style=utils.gui.get_slider_style()
        )

        @back_button.event("on_click")
        def on_click_back_button(event) -> None:
            logging.debug(event)

            # Pass already created view because we are resuming.
            self.on_back()

        @master_slider.event('on_change')
        def on_change_master_volume(event) -> None:
            logging.debug(event)

            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._master_volume = volume
            self.previous_view.previous_view.player.volume = self.state.settings._music_volume * volume

            self.state.settings.save()

        @music_slider.event('on_change')
        def on_change_music_volume(event) -> None:
            logging.debug(event)

            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._music_volume = volume
            self.previous_view.previous_view.player.volume = self.state.settings._master_volume * volume

            self.state.settings.save()

        @sound_slider.event("on_change")
        def on_change_sound_volume(event) -> None:

            logging.debug(event)

            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._sound_volume = volume
            self.state.settings.save()

        @atmo_slider.event("on_change")
        def on_change_atmo_volume(event) -> None:

            logging.debug(event)

            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._atmo_volume = volume
            self.state.settings.save()

        widgets = [
            back_button,
            master_label,
            master_slider,
            music_label,
            music_slider,
            sound_label,
            sound_slider,
            atmo_label,
            atmo_slider
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        On key press
        @param key: Key
        @param modifiers: Modifiers
        """

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time: float) -> None:
        """
        On update
        @param delta_time: Delta Time
        """

        super().on_update(delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ Render the screen. """

        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_back(self) -> None:
        """ Back button clicked """

        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)
