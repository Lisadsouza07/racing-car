import pygame
from game2 import *
from menu import *


class Game:
    def __init__(self):
        self.running , self.playing = True,False
        self.FPS = 60
        self.width, self.height = width,height
        self.BLACK = (0, 0, 0)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.playing = True
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.BACK_KEY = False
        self.ENTER_KEY = False
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing,self.running = False,False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.display.blit(text_surface, text_rect)

    def run_game(self):
        while self.playing:
            self.curr_menu.display_menu()
            self.curr_menu.run_display = True
            while self.curr_menu.run_display:
                self.check_events()
                self.curr_menu.check_input()
                self.display.fill(self.BLACK)
                self.curr_menu.blit_screen()
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.clock.tick(self.FPS)
            self.game_loop()


    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.ENTER_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
   

            draw(self.display, images, player_car, game_info)

            while not game_info.started:
                blit_text_center(self.display, main_font, f'Press any key to start {game_info.level}!')
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()





