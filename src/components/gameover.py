import pygame
import os
from components.component import Component
import pygame_menu
import utils.savegame
import utils.image


class GameOver(Component):

    def __init__(self, data_dir, handle_change_component):
        """ Constructor """
        super().__init__(data_dir, handle_change_component)
        self.menu = None

        file = os.path.join(data_dir, 'images', 'menu', 'gameover.jpg')

        self.backdrop = self.image_cache.load_image(file)

    def mount(self):
        # CREDITS: https://audionautix.com/creative-commons-music
        self.play_music('gameover.ogg', 0)

    def draw_background(self):
        self.screen.blit(self.backdrop, (0, 0))

    # Todo refactor to own class
    def update_screen(self, screen):
        self.backdrop = pygame.transform.smoothscale(
            self.backdrop, screen.get_size())
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title='Game Over',
                                width=400)

        if utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.state):
            menu.add.button('Load Game', self.load_game)  # Load save game
        menu.add.button('Back To Main Menu',
                        self.back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen, self.draw_background)

    def load_game(self):
        self.menu.disable()
        component = self.handle_change_component(None)
        component.handle_continue_game()

    def back_to_main_menu(self):
        self.menu.disable()
        self.handle_change_component(None)
