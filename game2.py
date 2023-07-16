import sys
import pygame
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center
from game import Game

pygame.font.init()

DIRT = scale_image(pygame.image.load('Background/dirt2.jpg'), 1.1)
track = scale_image(pygame.image.load('Background/Race track1.png'), 1.1)
track_border = scale_image(pygame.image.load('Background/Trackempty3.png'), 1.1)
track_border_mask = pygame.mask.from_surface(track_border)
finish = scale_image(pygame.image.load('icons/finish.png'), 0.70)
finish_mask = pygame.mask.from_surface(finish)
finish_position = (110, 263)
blue_car = scale_image(pygame.image.load('icons/car_blue.png'), 0.20)
bg = pygame.image.load('Background/Grass.jpg')

width, height = track.get_width(), track.get_height()
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption('Motion Master')

main_font = pygame.font.SysFont('Calibri', 30)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("icons/Roboto-Black.ttf", size)


FPS = 60

class GameInfo():
    Levels = 5

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.Levels

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = min(self.vel + self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):

    IMG = blue_car
    START_POS = (134, 280)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

def game_loop(self):
    game_info = GameInfo()
    player_car = PlayerCar(4, 4)
    images = [(DIRT, (0, 0)), (track, (0, 0)), (finish, finish_position), (track_border, (0, 0))]

    while self.playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                sys.exit()


def draw(win, images, player_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = main_font.render(f'Level: {game_info.level}', 1, (255, 255, 255))
    win.blit(level_text, (10, height - level_text.get_height() - 70))

    time_text = main_font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, height - time_text.get_height() - 40))

    vel_text = main_font.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, height - vel_text.get_height() - 10))

    player_car.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    # If right arrow key is pressed
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    # If left arrow key is pressed
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    # If up arrow key is pressed
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_backward()
    # If down arrow key is pressed
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_forward()

    if not moved:
        player_car.reduce_speed()




def handle_collision(player_car, game_info):
    if player_car.collide(track_border_mask) is not None:
        player_car.bounce()
    player_finish_poi_collide = player_car.collide(finish_mask, *finish_position)
    if player_finish_poi_collide is not None:
        blit_text_center(WIN, main_font, 'You Lost!')
        pygame.time.wait(5000)
        if player_finish_poi_collide[1] == 0.9:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            player_car.next_level(game_info.level)


            move_player(player_car)
            handle_collision(player_car, game_info)

            if game_info.game_finished():
                blit_text_center(self.display, main_font, 'You Won!')
                pygame.time.wait(5000)
                game_info.reset()
                player_car.reset()

            draw(self.display, images, player_car, game_info)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)



if __name__ == '__main__':
    game = Game()
    game.run_game()



