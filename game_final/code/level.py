import pygame
from tiles import Tile
from settings import tile_size
from player import Player


class Level:
    def __init__(self, level_data, surface):

        # настройки уровня
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0  # переменная для движения карты
        self.current_x = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()  # группа для блоков
        self.player = pygame.sprite.GroupSingle()  # группа для игрока
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):  # цикл для перебора всех элементов карты уровня
                x = col_index * tile_size
                y = row_index * tile_size  # координаты, в которых будут находиться выводимые объекты

                if cell == 'X':  # если элемент в карте уровня X

                    tile = Tile((x, y), tile_size)  # плитка с нужными координатами и размером
                    self.tiles.add(tile)  # в группу для блоков добавляется эта плитка
                if cell == 'P':  # если элемент в карте уровня P
                    player_sprite = Player((x, y))  # игрок с нужными координатами
                    self.player.add(player_sprite)  # в группу для игрока добавляется этот игрок

    # движение игрока
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx  # положение игрока
        direction_x = player.direction.x  # направление движения игрока

        if player_x < 200 and direction_x < 0:  # граница, за которой вместо движения игрока влево движется карта уровня
            self.world_shift = 8  # скорость движения карты уровня
            player.speed = 0  # скорость движения игрока
        elif player_x > 1050 and direction_x > 0:  # граница, за которой игрок не движется, движется карта уровня
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0  # в других случаях игрок двигается
            player.speed = 8

    # работа с горизонтальными коллизиями
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed    # обновление позиции - изменение координаты по горизонтали

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # проверка коллизий блоков и игрока
                if player.direction.x < 0:  # если игрок двигается влево
                    player.rect.left = sprite.rect.right  # его левая координата остаётся равной правой координате блока
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:  # если игрок двигается вправо
                    player.rect.right = sprite.rect.left  # его правая координата остаётся равной левой координате блока
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    # работа с вертикальными коллизиями
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # проверка коллизий блоков и игрока
                if player.direction.y > 0:  # если игрок двигается вниз
                    player.rect.bottom = sprite.rect.top  # нижняя координата остаётся равной верхней координате блока
                    player.direction.y = 0  # гравитация обнуляется при наличии препятствия снизу
                    player.on_ground = True  # игрок стоит на поверхности
                elif player.direction.y < 0:  # если игрок двигается вверх
                    player.rect.top = sprite.rect.bottom  # верхняя координата остаётся равной нижней координате блока
                    player.direction.y = 0  # при касании верхнего препятствия гравитация тоже обнуляется
                    player.on_ceiling = True  # игрок касается блока свеху
        if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False  # игрок больше не стоит на поверхности
        if player.on_ceiling and (player.direction.y < 0 or player.direction.y > 0):
            player.on_ceiling = False  # игрок больше не касается блока сверху

    # вывод всего на экран
    def run(self):

        # блоки
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # игрок
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
