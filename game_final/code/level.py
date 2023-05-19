import pygame
import os
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Coin
from enemy import *
from player import Player
from particles import ParticleEffect
from decoration import Forest


class Level:
    def __init__(self, level_data, surface, change_coins, change_health):  # информация об уровне

        # общие настройки
        self.display_surface = surface
        self.world_shift = 0  # интенсивность скроллинга
        self.current_x = None

        # игрок в начале и в конце уровня
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # user interface
        self.max_level = 2  # сначала доступно 3 уровня
        self.max_health = 100  # максимальный процент жизни
        self.cur_health = 100  # процент жизни
        self.coins = 0  # количество монет

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()  # добавляем взрывы, когда герой сталкивается с врагом

        # фон
        self.forest = Forest()

        # настройка местности
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # настройка травы
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # монеты
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # враги
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # ограничения для врагов (чтобы меняли траекторию движения, натыкаясь на них)
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        # у каждого элемента такой же индекс в списке, как и ID в программе Tiled. Поэтому:
                        tile_surface = terrain_tile_list[int(val)]  # берем соответствующий тайл в завис-ти от числа
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':  # делаем то же самое с травой
                        grass_tile_list = import_cut_graphics('../graphics/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'coins':
                        sprite = Coin(tile_size, x, y, '../graphics/coins/gold')

                    if type == 'enemies':  # Каждому ID врага из Tiled приписываем соотв класс с соотв изображениями
                        if val == '0':
                            sprite = Black(tile_size, x, y)
                        # Например, если ID = 0 (а в Tiled черный враг имеет ID = 0), то мы используем класс, который
                        # ведёт к папке с изображениями черного врага. С остальными врагами всё аналогично.
                        if val == '2':
                            sprite = Green(tile_size, x, y)
                        if val == '3':
                            sprite = Mushroom(tile_size, x, y)
                        if val == '4':
                            sprite = Red(tile_size, x, y)

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), change_health)
                    self.player.add(sprite)
                if val == '1':
                    diamond_surface = pygame.image.load('../graphics/player/diamond.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, diamond_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):  # чтобы враги могли ударяться о невидимые блоки, меняющие траекторию их движения
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # работа с горизонтальными коллизиями
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed  # обновление позиции - изменение координаты по горизонтали

        for sprite in self.terrain_sprites.sprites():
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

        for sprite in self.terrain_sprites.sprites():
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

    # движение игрока (скроллинг)
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx  # положение игрока
        direction_x = player.direction.x  # направление движения игрока

        if player_x < 400 and direction_x < 0:  # граница, за которой вместо движения игрока влево движется карта уровня
            self.world_shift = 5  # скорость движения карты уровня
            player.speed = 0  # скорость движения игрока
        elif player_x > 650 and direction_x > 0:  # граница, за которой игрок не движется, движется карта уровня
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0  # в других случаях игрок двигается
            player.speed = 5

    def check_death(self):
        game_active = True
        if self.player.sprite.rect.top > screen_height or self.cur_health <= 0:
            game_active = False
        return game_active

    def check_win(self):
        win = False
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            win = True
        return win

    def check_coin_collisions(self):  # смотрим на то, поймал ли герой монету
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)

    def change_coins(self, amount):  # меняем количество монет
        self.coins += amount

    def check_enemy_collisions(self):  # смотрим на то, столкнулся ли герой с врагом
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:  # если герой задевает врага сверху
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:  # проверяем, что
                    self.player.sprite.direction.y = -15  # герой двигается вниз и касается нижней своей частью
                    # верхней части врага
                    enemy.kill()
                else:
                    self.change_health(self.player.sprite.get_damage())  # если герой задевает врага сбоку

    def change_health(self, amount):  # меняем уровень жизни
        self.cur_health += 16 * amount

    def run(self):  # мы будем запускать всю игру с помощью этой функции
        # Строчки, которые расположены ниже, накладываются на строчки, расположенные выше.
        # Таким образом, враги накладываются на местность, трава - на врагов и на местность, и т.п.

        # фон
        self.forest.update(self.world_shift)
        self.forest.draw(self.display_surface)

        # местность
        self.terrain_sprites.update(self.world_shift)  # скорость скроллинга
        self.terrain_sprites.draw(self.display_surface)

        # враги
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # трава
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # монеты
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # настройки игрока
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_coin_collisions()
        self.check_enemy_collisions()

        self.check_death()
        self.check_win()
