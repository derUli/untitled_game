import pygame

from components.menucomponent import SettingsComponent
from constants.quality import QUALITY_OFF, QUALITY_MEDIUM, QUALITY_HIGH
from utils.menu import make_menu, get_longest_option
from utils.render_cache import store_clear


MIN_SCREEN_RESOLUTION = (800, 600)


class SettingsScreen(SettingsComponent):
    def handle_change_screen_resolution(self, selection, selected_index):
        """ Handle change resolution """
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.screen_resolution = value
        self.settings_state.apply_and_save()
        self.settings_state.needs_restart = True
        store_clear()

    def handle_toggle_fullscreen(self, value):
        """ Handle toggle fullscreen """
        self.settings_state.fullscreen = value
        self.settings_state.apply_and_save()

    def handle_toggle_vsync(self, value):
        """ Handle toggle VSync """
        self.settings_state.vsync = value
        self.settings_state.apply_and_save()
        self.settings_state.needs_restart = True

    def get_screen_resolution_items(self):
        """ Get screen resolution items """
        modes = pygame.display.list_modes()

        # If the current screen resolution is not in supported modes add it
        if self.settings_state.screen_resolution not in modes:
            modes.append(self.settings_state.screen_resolution)

        modes = sorted(modes)

        items = []
        for x, y in modes:
            # Screen resolutions lower than this would crash
            if (x, y) < MIN_SCREEN_RESOLUTION:
                continue

            label = (str(x) + 'x' + str(y))
            value = (x, y)
            items.append((label, value))

        return items

    def draw_menu(self, screen):
        menu = make_menu(_('Screen'), self.settings_state.limit_fps)

        state_text = (_('Off'), _('On'))

        menu.add.toggle_switch(
            _('Fullscreen'),
            self.settings_state.fullscreen,
            self.handle_toggle_fullscreen,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('V-Sync'),
            self.settings_state.vsync,
            self.handle_toggle_vsync,
            state_text=state_text
        )

        menu.add.dropselect(
            title=_('Screen Resolution'),
            default=self.get_selected_index(
                self.get_screen_resolution_items(),
                self.settings_state.screen_resolution),
            items=self.get_screen_resolution_items(),
            onchange=self.handle_change_screen_resolution,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_screen_resolution_items()),
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
