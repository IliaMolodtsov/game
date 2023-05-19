import pygame
import sys
from settings import *
from level import Level
from game_data import level_0
from ui import UI
from menu import menu
from menu import print_text


class Game:
    def __init__(self):

        # интерфейс пользователя
        self.ui = UI(screen)

    def run(self):
        self.ui.show_health(level.cur_health, level.max_health)
        self.ui.show_coins(level.coins)


# Создаем экран
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Call of the soul")
icon = pygame.image.load('../graphics/icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()  # Это часы на будущее, чтобы регулировать смену кадров движения привидения
level = Level(level_0, screen, 1, 1)
game = Game()

menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if level.check_death():
        screen.fill('grey')
        level.run()
        game.run()
        if level.check_win():
            game_win_screen = pygame.image.load('../graphics/screens/menu.jpg').convert_alpha()
            screen.blit(game_win_screen, (0, 0))
            print_text('congratulations! you won!', 250, 270, font_color=(255, 255, 255),
                       font_type="../graphics/fonts/Sonic Filled.ttf",
                       font_size=30)
    else:
        game_over_screen = pygame.image.load('../graphics/screens/menu.jpg').convert_alpha()
        screen.blit(game_over_screen, (0, 0))
        print_text('game over', 480, 190, font_color=(255, 255, 255), font_type="../graphics/fonts/Sonic Filled.ttf",
                   font_size=30)

    pygame.display.update()
    clock.tick(60)  # указываем количество фреймов за 1 сек, т.е. количество раз, которое проиграется цикл за 1 сек
