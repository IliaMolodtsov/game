import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):  # класс для квадратов, которые будут на экране
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):  # делаем возможность скроллинга
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.1  # скорость изменения изображений при анимации
        if self.frame_index >= len(self.frames):  # обнуляем индекс, когда доходим до конца, чтобы не выйти за пределы
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):  # подправляем местоположение монет
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)  # двигаем монеты в центр тайла
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
