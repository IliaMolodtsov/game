import pygame
from tiles import AnimatedTile

# Так как у нас несколько типов врагов, мы создадим несколько классов, которые будут вести к своей папке с врагом


class Red(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemies/runner_left')
        self.rect.y += 6  # поначалу персонаж из-за особенностей своего изображения появляется выше положенного места.
        # В строке 10 мы исправляем это, меняя его координаты y. Теперь персонаж стоит ниже, чем раньше,
        # в нужном нам месте. Чем больше натуральное число, тем ниже опускается персонаж.
        self.speed = 4  # скорость движения врага

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):  # функция для того, чтобы, когда враг бежал не влево, а вправо, его изображение
        # тоже отзеркаливалось вправо
        if self.speed > 0:  # если враг идёт вправо
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()  # это из класса AnimatedTile
        self.move()
        self.reverse_image()


class Green(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemies/enemy_sky_left')
        self.rect.y -= 20  # ставим зеленого врага повыше.
        self.speed = 3

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):  # функция для того, чтобы, когда враг бежал не влево, а вправо, его изображение
        # тоже отзеркаливалось вправо
        if self.speed > 0:  # если враг идёт вправо
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()  # это из класса AnimatedTile
        self.move()
        self.reverse_image()


class Black(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemies/enemy_land_left')
        self.rect.y -= 24  # ставим черного врага выше.
        self.speed = 2

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):  # функция для того, чтобы, когда враг бежал не влево, а вправо, его изображение
        # тоже отзеркаливалось вправо
        if self.speed > 0:  # если враг идёт вправо
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()  # это из класса AnimatedTile
        self.move()
        self.reverse_image()


class Mushroom(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemies/mushroom')
        self.rect.y -= 125  # ставим гриба выше. Чем больше отрицательное число, тем выше поднимается гриб.
