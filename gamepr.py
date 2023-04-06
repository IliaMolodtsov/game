import pygame

clock = pygame.time.Clock()  # Это часы на будущее, чтобы регулировать смену кадров движения привидения

pygame.init()
screen = pygame.display.set_mode((1099, 669))
pygame.display.set_caption("proga")
icon = pygame.image.load('images/Ghost-64.webp')
pygame.display.set_icon(icon)

# АНИМАЦИЯ И ДВИЖЕНИЕ ГГ

walk_right = [
    pygame.image.load('images/player_right/player_right1.png'),
    pygame.image.load('images/player_right/player_right2.png')
]  # список из подключенных картинок привидения, идущего направо
walk_left = [
    pygame.image.load('images/player_left/player_left1.png'),
    pygame.image.load('images/player_left/player_left2.png')
]  # список из подключенных картинок привидения, идущего налево

player_anim_count = 0  # счетчик-индекс для изображений в списке анимаций игрока
player_speed = 10  # это будем отнимать и прибавлять к координатам по х, тем самым регулируя скорость игрок
player_x = 150  # координаты игрока по х
player_y = 540  # координаты игрока по y. Чем больше координаты, тем НИЖЕ ИГРОК. Чем меньше координаты, тем игрок ВЫШЕ.

is_jump = False  # переменная для отслеживания прыжка
jump_count = 10  # количество позиций, на которое мы будем поднимать игрока при прыжке (высота прыжка)


# БЭКГРАУНД
bg = pygame.image.load('images/pixel_bg.png')

bg_x = 0

# ВНЕДРЕНИЕ ВСЕГО В ИГРУ

running = True
while running:

    # НАСТРОЙКА БЭКГРАУНДА

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1099, 0))

    bg_x -= 1  # настраиваем скорость движения бэкграунда
    if bg_x == -1099:
        bg_x = 0

    # ВНЕДРЕНИЕ ИГРОКА И НАСТРОЙКА ЕГО АНИМАЦИИ

    player = pygame.image.load('images/player_right/player_right1.png')  # базовая картинка игрока
    keys = pygame.key.get_pressed()  # Кнопка, на которую сейчас нажимает пользователь
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    # Выводим на экран игрока с указанием его координат,
    # при этом выводя все элементы списка по индексу указанной в кв скобках переменной. Это для эффекта движения влево
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
        # это то же самое, но для эффекта движения вправо
    else:
        screen.blit(player, (player_x, player_y))  # делаем такую картинку когда игрок стоит
    # строчки ниже - настройка индексов анимаций игрока
    if player_anim_count == 1:  # Обнуляем индекс, когда доходим до последнего элемента списка (чтобы не выйти за него)
        player_anim_count = 0
    else:
        player_anim_count += 1  # каждый раз, заходя в цикл, будем увеличивать индекс, выводя поочередно все элементы

    # НАСТРОЙКА ДВИЖЕНИЯ И ПРЫЖКА ИГРОКА

    if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_x > 20:
        # Если эта кнопка равна стрелке влево или букве A, да и коорд игр больше 50 (невидимая граница слева), то:
        player_x -= player_speed  # движемся влево, вычитая показатели из координат игрока
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x < 1039:
        # Если эта кнопка равна стрелке вправо или букве D, да и коорд игр меньше 649 (невидимая граница справа), то:
        player_x += player_speed  # движемся вправо, прибавляя показатели к координатам игрока

    if not is_jump:  # Если наш герой в данный момент не прыгает, то:
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:  # при наж на пробел / W / стрелку вверх:
            is_jump = True  # значение прыжка активируется и герой должен прыгнуть
    else:  # если значение прыжка активируется, то:
        if jump_count >= -10:  # покуда всё больше -10, процесс прыжка идёт
            if jump_count >= 0:  # для поднятия
                player_y -= (jump_count ** 2) / 2  # Возводим в квадрат для БОЛЬШЕЙ МОЩИ! Делим на 2 для плавного эффек.
                # поднимаем игрока, постепенны отнимая числа от его координат
            else:  # для опускания
                player_y += (jump_count ** 2) / 2  # опускаем игрока
            jump_count -= 1  # постепенно отнимаем 1 для плавного перемещения игрока вверх и обратно.
        else:  # если дошли до -10, то прыжок уже сделан, можно вернуть все параметры к старым значениям.
            is_jump = False
            jump_count = 10

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(20)  # указываем количество фреймов за 1 сек, т.е. количество раз, которое проиграется цикл за 1 сек
    # иначе говоря, скорость смены изображений-анимаций игрока.