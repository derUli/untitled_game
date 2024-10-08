import argparse
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk

from constants.audio import audio_backends
from constants.settings import QualityPreset
from state.settingsstate import SettingsState
from utils.media.video import video_supported
from utils.screen import supported_screen_resolutions

NOTEBOOK_PADDING = 10

SPACE_BETWEEN_X = 2
SPACE_BETWEEN_Y = 5

TTK_THEME = 'equilux'


class LauncherWindow(ThemedTk):
    def __init__(self, theme: str = TTK_THEME, args=None, state=None):
        super().__init__(theme=theme)

        self.path_state = state
        self.args = args

        self.fullscreen = tk.BooleanVar(value=args.fullscreen)

        self.screen_resolution = tk.StringVar(
            value=str(args.width) + 'x' + str(args.height)
        )

        self.vsync = tk.BooleanVar(value=not args.no_vsync)

        quality = args.video_quality
        if quality is None:
            quality = 4

        preset = QualityPreset(quality)

        self.quality = tk.IntVar(value=quality)
        self.filmgrain = tk.DoubleVar(value=preset.filmgrain)
        self.antialiasing = tk.IntVar(value=preset.antialiasing)
        self.weather = tk.BooleanVar(value=preset.weather)
        self.colortint = tk.BooleanVar(value=preset.color_tint)
        self.videos = tk.BooleanVar(value=True)

        self.audio_backend = tk.StringVar(value=args.audio_backend)
        self.state = SettingsState()
        self.confirmed = False

        self.weather_check = None
        self.color_tint_check = None

    def setup(self) -> None:
        """
        Set up the UI
        """
        self.title(_('Grunzi'))
        self.bind_keyevents()
        self.set_icon()

        if SettingsState.exists():
            self.state = SettingsState.load()

            self.fullscreen.set(self.state.fullscreen)
            self.vsync.set(self.state.vsync)
            self.quality.set(self.state.quality)
            self.antialiasing.set(self.state.antialiasing)
            self.filmgrain.set(self.state.filmgrain)
            self.weather.set(self.state.weather)
            self.colortint.set(self.state.color_tint)
            self.videos.set(self.state.videos)

            w, h = self.state.screen_resolution[0], self.state.screen_resolution[1]
            self.screen_resolution.set(
                value=str(w) + 'x' + str(h)
            )

            self.audio_backend.set(self.state.audio_backend)

        # Detect screen resolution on first start
        if not self.state.first_start:
            self.screen_resolution.set(supported_screen_resolutions()[-1])

        tab_control = ttk.Notebook(self)

        tab_screen = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)

        tab_graphics = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)
        tab_audio = ttk.Frame(tab_control, padding=NOTEBOOK_PADDING)

        tab_control.add(tab_screen, text=_('Screen'))
        tab_control.add(tab_graphics, text=_('Graphics'))
        tab_control.add(tab_audio, text=_('Audio'))
        tab_control.pack(expand=True, fill=tk.BOTH)

        ttk.Label(tab_screen, text=_('Screen resolution') + ' ').grid(
            row=0,
            column=0,
            padx=SPACE_BETWEEN_X,
            pady=SPACE_BETWEEN_Y,
            sticky=tk.W
        )

        ttk.Combobox(
            tab_screen,
            values=supported_screen_resolutions(),
            textvariable=self.screen_resolution,
            state='readonly'
        ).grid(row=0, column=1, pady=SPACE_BETWEEN_Y, sticky=tk.E)

        ttk.Checkbutton(
            tab_screen,
            text=_('Fullscreen'),
            variable=self.fullscreen,
            onvalue=True,
            offvalue=False,
        ).grid(row=1, column=0, pady=SPACE_BETWEEN_Y, sticky=tk.W)

        ttk.Checkbutton(tab_screen,
                        text=_('V-Sync'),
                        variable=self.vsync,
                        onvalue=True,
                        offvalue=False
                        ).grid(row=3, column=0, pady=SPACE_BETWEEN_Y, sticky=tk.W)

        ttk.Label(tab_graphics, text=_('Quality') + ' ').grid(
            row=0,
            column=0,
            pady=SPACE_BETWEEN_Y,
            sticky=tk.W
        )

        (ttk.Scale(tab_graphics, from_=0, to=6, variable=self.quality, command=self.on_change_quality)
         .grid(row=0, column=1, pady=SPACE_BETWEEN_Y, sticky=tk.E))

        ttk.Label(tab_graphics, text=_('Antialiasing') + ' ').grid(
            row=1,
            column=0,
            pady=SPACE_BETWEEN_Y,
            sticky=tk.W
        )

        (ttk.Scale(tab_graphics, from_=0, to=16, variable=self.antialiasing)
         .grid(row=1, column=1, pady=SPACE_BETWEEN_Y, sticky=tk.E))

        ttk.Label(tab_graphics, text=_('Film Grain') + ' ').grid(
            row=2,
            column=0,
            pady=SPACE_BETWEEN_Y,
            sticky=tk.W
        )

        (ttk.Scale(tab_graphics, from_=0, to=1, variable=self.filmgrain)
         .grid(row=2, column=1, pady=SPACE_BETWEEN_Y, sticky=tk.E))

        self.weather_check = ttk.Checkbutton(
            tab_graphics,
            text=_('Weather'),
            variable=self.weather,
            onvalue=True,
            offvalue=False,
        )

        self.weather_check.grid(row=3, column=0, pady=SPACE_BETWEEN_Y, sticky=tk.W)

        ttk.Checkbutton(
            tab_graphics,
            text=_('Color Tint'),
            variable=self.colortint,
            onvalue=True,
            offvalue=False,
        ).grid(row=4, column=0, pady=SPACE_BETWEEN_Y, sticky=tk.W)

        videos_state = tk.NORMAL

        if not video_supported():
            videos_state = tk.DISABLED

        ttk.Checkbutton(
            tab_graphics,
            text=_('Videos'),
            variable=self.videos,
            onvalue=True,
            offvalue=False,
            state=videos_state
        ).grid(row=5, column=0, pady=SPACE_BETWEEN_Y, sticky=tk.W)

        ttk.Label(tab_audio, text=_('Audio Backend') + ' ').grid(
            row=0,
            column=0,
            pady=SPACE_BETWEEN_Y,
            sticky=tk.W
        )

        ttk.Combobox(
            tab_audio,
            values=audio_backends(),
            textvariable=self.audio_backend,
            state='readonly'
        ).grid(row=0, column=1, pady=SPACE_BETWEEN_Y, sticky=tk.E)

        button_launch = ttk.Button(text=_('Launch Game'), command=self.on_launch)

        button_launch.pack(expand=True, fill=tk.BOTH, ipady=10)

        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        button_launch.focus_set()

    def bind_keyevents(self) -> None:
        """ Bind keyboard events"""

        # ESC key will quit the app
        self.bind('<Escape>', lambda e: self.destroy())

        # RETURN key will start the game
        self.bind('<Return>', self.on_launch)

    def set_icon(self) -> None:
        """
        Set window icon
        """
        icon = PhotoImage(file=os.path.join(self.path_state.ui_dir, 'icon.ico'))
        self.tk.call('wm', 'iconphoto', self._w, icon)

    def get_args(self) -> argparse.Namespace | None:
        """
        Apply selected settings to args
        @return: Argparse Namespace
        """

        if not self.confirmed:
            return None

        # Apply settings in state
        self.state.fullscreen = self.fullscreen.get()
        self.state.videos = self.videos.get()
        self.state.vsync = self.vsync.get()

        if self.state.quality != self.quality.get():
            self.state.quality = self.quality.get()
            self.args.video_quality = self.quality.get()

        if self.state.antialiasing != self.antialiasing.get():
            self.state.antialiasing = self.antialiasing.get()
            self.args.antialiasing = self.state.antialiasing

        self.state.filmgrain = self.filmgrain.get()
        self.state.weather = self.weather.get()
        self.state.color_tint = self.colortint.get()

        w, h = self.screen_resolution.get().split('x')
        self.state.screen_resolution = [w, h]
        self.state.audio_backend = self.audio_backend.get()
        self.state.first_start = True
        self.state.save()

        # Apply settings to args
        self.args.fullscreen = self.fullscreen.get()
        self.args.window = not self.fullscreen.get()
        self.args.no_vsync = not self.vsync.get()

        screen_resolution = self.screen_resolution.get().split('x')

        self.args.width = int(screen_resolution[0])
        self.args.height = int(screen_resolution[1])

        self.args.audio_backend = self.audio_backend.get()

        return self.args

    def on_launch(self, event=None):
        logging.debug(event)

        self.confirmed = True
        self.state.save()
        self.destroy()

    def on_change_quality(self, value):
        rounded = int(float(value))
        self.state.quality = rounded
        self.filmgrain.set(self.state.filmgrain)
        self.antialiasing.set(self.state.antialiasing)
        self.weather.set(self.state.weather)
        self.colortint.set(self.state.color_tint)
