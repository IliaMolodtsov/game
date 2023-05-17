import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['player_right'][self.frame_index]  # изображение персонажа
        self.rect = self.image.get_rect(topleft=pos)

        # движение персонажа
        self.direction = pygame.math.Vector2(0, 0)  # направление движения с помощью вектора
        self.speed = 8  # скорость персонажа
        self.gravity = 0.8  # значение гравитации
        self.jump_speed = -16  # начальная величина прыжка

        # положение игрока
        self.status = 'player_right'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'player_right': [], 'player_left': []}  # словарь с изображениями из папки

        for animation in self.animations.keys():  # берём каждое название внутри папки
            full_path = character_path + animation  # путь к файлу
            self.animations[animation] = import_folder(full_path)  # получаем название файла внутри данной папки

    def animate(self):
        animation = self.animations[self.status]  # берётся одна папка с картинками

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

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
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

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
