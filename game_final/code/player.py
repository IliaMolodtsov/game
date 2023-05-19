import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['player_right'][self.frame_index]  # изображение персонажа
        self.rect = self.image.get_rect(topleft=pos)

        # движение персонажа
        self.direction = pygame.math.Vector2(0, 0)  # направление движения с помощью вектора
        self.speed = 5  # скорость персонажа
        self.gravity = 0.8  # значение гравитации
        self.jump_speed = -20  # начальная величина прыжка

        # положение игрока
        self.status = 'player_right'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # управление изменением шкалы жизни
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

    def import_character_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'player_right': [], 'player_left': []}  # словарь с изображениями из папки

        for animation in self.animations.keys():  # берём каждое название внутри папки
            full_path = character_path + animation  # путь к файлу
            self.animations[animation] = import_folder(full_path)  # получаем название файла внутри данной папки

    def animate(self):  # отслеживаем мигание игрока при встрече с врагами
        animation = self.animations[self.status]  # берётся одна папка с картинками

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        # изменение frame_index
        if self.direction.x != 0:  # нужно только когда происходит движение вправо или влево
            self.frame_index += self.animation_speed  # индекс увеличивается
            if self.frame_index >= len(animation):
                self.frame_index = 0

        self.image = animation[int(self.frame_index)]  # картинка до тех пор, пока индекс не увеличится на единицу

        # настройка области игрока
        # для каждой из ситуаций касания блоков устанавливается точка, от которой отсчитываются координаты
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.bottomright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.bottomleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midbottom)

    # отслеживание нажатия клавиш
    def get_input(self):
        keys = pygame.key.get_pressed()  # какие клавиши нажаты

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1  # направление движения вправо
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1  # направление движения влево
            self.facing_right = False
        else:
            self.direction.x = 0  # нет движения

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()

    def get_status(self):
        if self.facing_right:
            self.status = 'player_right'
        else:
            self.status = 'player_left'

    def apply_gravity(self):
        self.direction.y += self.gravity  # координата движения по вертикали увеличивается
        self.rect.y += self.direction.y  # координата увеличивается

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):  # повреждения
        if not self.invincible:
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            return -1
        else:
            return 0

    def invincibility_timer(self):  # мигание
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()
