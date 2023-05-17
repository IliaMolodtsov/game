import pygame
import sys
from settings import *
from level import Level

# настройка pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # Это часы на будущее, чтобы регулировать смену кадров движения привидения
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)  # указываем количество фреймов за 1 сек, т.е. количество раз, которое проиграется цикл за 1 сек
    # иначе говоря, скорость смены изображений-анимаций игрока.
