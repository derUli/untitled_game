import logging
import os

import arcade.gui

import utils.text
from views.fading import Fading
from views.optionsmenu import OptionsMenu

BUTTON_WIDTH = 250
BUTTON_MARGIN_BOTTOM = 20


class MainMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state):
        super().__init__(window)

        self.window = window
        self.state = state

        self.manager = arcade.gui.UIManager(window)

        label = arcade.gui.UILabel(
            text=_('Grunzi'),
            #font_name=utils.text.ADRIP_FONT,
            font_size=utils.text.LOGO_FONT_SIZE,
            text_color=arcade.csscolor.HOTPINK,
            align='center'
        )

        newgame_button = arcade.gui.UIFlatButton(
            text=_("New Game"),
            width=BUTTON_WIDTH,
            #stye=utils.text.get_style()
        )

        options_help = arcade.gui.UIFlatButton(
            text=_("Options & Help"),
            width=BUTTON_WIDTH,
            #stye=utils.text.get_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Quit game"),
            width=BUTTON_WIDTH,
            #style=utils.text.get_style()
        )

        self.player = None

        size = self.window.size()
        self.shadertoy = self.state.load_shader(size, 'pigs')

        self.time = 0

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            # Pass already created view because we are resuming.

            from views.game import Game
            self.next_view = Game(self.window, self.state)
            self.fade_out()

        @options_help.event("on_click")
        def on_click_options_help(event):
            # Pass already created view because we are resuming.

            self.window.show_view(
                OptionsMenu(self.window, self.state, previous_view=self, shadertoy=self.shadertoy, time=self.time)
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.fade_quit()

        buttons = [
            label,
            newgame_button,
            options_help,
            quit_button
        ]

        # Initialise a grid in which widgets can be arranged.
        self.grid = arcade.gui.UIGridLayout(
            column_count=1,
            row_count=4,
            horizontal_spacing=20,
            vertical_spacing=20,
            align_horizontal="center",
            align_vertical="center"
        )

        # Adding the buttons to the layout.
        self.grid.add(label, col_num=0, row_num=0)
        self.grid.add(newgame_button, col_num=0, row_num=1)
        self.grid.add(options_help, col_num=0, row_num=2)
        self.grid.add(quit_button, col_num=0, row_num=3)

        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(
            arcade.gui.UIAnchorLayout(
        ))

        self.anchor.add(
            child=self.grid,
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

        if self.next_view:
            if self.player:
                self.player.pause()

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        music = None

        try:
            music = arcade.load_sound(os.path.join(self.state.music_dir, 'menu.ogg'))
        except FileNotFoundError as e:
            logging.error(e)

        if not self.player and music:
            self.player = music.play(loop=True, volume=self.state.music_volume)

        self.manager.enable()

    def on_update(self, dt):
        self.time += dt
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        self.shadertoy.render(time=self.time)

        self.manager.draw()
        self.draw_build_version()

        self.draw_fading()
        self.draw_debug()
