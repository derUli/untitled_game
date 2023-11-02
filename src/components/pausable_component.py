import pygame
import pygame_menu
import utils.savegame
import gettext

_ = gettext.gettext


class PausableComponent():

    # Todo refactor to own class
    def pause_menu(self):

        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title='Pause menu',
                                width=self.screen.get_width() / 3)

        menu.add.button(_('Continue'), self.handle_continue_game)  # Continue game
        menu.add.button(_('Save Game'), self.handle_save_game)  # Continue game
        menu.add.button(_('Back To Main Menu'),
                        self.back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen)

    def handle_continue_game(self):
        self.menu.disable()
        pygame.mouse.set_visible(0)

    def handle_save_game(self):
        utils.savegame.save_game(utils.savegame.DEFAULT_SAVE, self.state)
        self.handle_continue_game()

    def back_to_main_menu(self):
        self.handle_continue_game()
        pygame.mouse.set_visible(1)
        self.handle_change_component(None)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_menu()
            return

        super().handle_event(event)
