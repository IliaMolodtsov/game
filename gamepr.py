import pygame
from pygame.locals import *

# Эта функция упрощает загрузку изображений
def img(filename):
    return pygame.image.load(f'images/{filename}')

clock = pygame.time.Clock()  # Это часы на будущее, чтобы регулировать смену кадров движения привидения

pygame.init()
screen = pygame.display.set_mode((1099, 669))
pygame.display.set_caption("proga")
icon = img('Ghost-64.webp')
pygame.display.set_icon(icon)

# АНИМАЦИЯ И ДВИЖЕНИЕ ГГ

walk_right = [
    img('player_right/player_right1.png'),
    img('player_right/player_right2.png')
]  # список из подключенных картинок привидения, идущего направо
walk_left = [
    img('player_left/player_left1.png'),
    img('player_left/player_left2.png')
]  # список из подключенных картинок привидения, идущего налево

player_anim_count = 0  # счетчик-индекс для изображений в списке анимаций игрока
player_speed = 10  # это будем отнимать и прибавлять к координатам по х, тем самым регулируя скорость игрока
player_x = 150  # координаты игрока по х
player_y = 540  # координаты игрока по y. Чем больше координаты, тем НИЖЕ ИГРОК. Чем меньше координаты, тем игрок ВЫШЕ.
frame_left = 70  # настраиваем координаты рамки для игрока
frame_right = 220

player_delay = 10  # количество кадров, через которое кадр анимации игрока сменяется
player_delay_frame = 0  # количество кадров прошедших с момента последней смены кадра

is_jump = False  # переменная для отслеживания прыжка
jump_count = 10  # количество позиций, на которое мы будем поднимать игрока при прыжке (высота прыжка)
turn_left = False  # переменная для отслеживания поворота игрока

player_lives = 5  # количество жизней игрока. Если игрок теряет все жизни, игра заканчивается
invincible = 0  # длина периода неуязвимости после получения урона, измеряется в кадрах

# ПУЛИ

bullet = img('bullet/bullet.png')  # картинка пули
bullets = []  # список, в который будут добавляться активные пули
bullets_left = 5  # счётчик количества пуль

# АНИМАЦИЯ И ДВИЖЕНИЕ НАЗЕМНОГО ВРАГА

enemy_land_left = [
    img('enemy_land_left/enemy_land_left1.png'),
    img('enemy_land_left/enemy_land_left2.png')
]  # список из подключенных картинок наземного врага, идущего налево
enemy_land_right = [
    img('enemy_land_right/enemy_land_right1.png'),
    img('enemy_land_right/enemy_land_right2.png')
]  # список из подключенных картинок наземного врага, идущего направо

# список из которого по значению enemy_land_dir будет выбрана анимация
# первый элемент пуст так как enemy_land_dir никогда не равна 0
enemy_land_anim = [0, enemy_land_right, enemy_land_left]

enemy_land_delay = 2  # количество кадров, через которое кадр анимации наземного врага сменяется
enemy_land_delay_frame = 0  # количество кадров прошедших с момента последней смены кадра

enemy_land_speed = 2  # это будем отнимать и прибавлять к координатам по х, тем самым регулируя скорость наземного врага
enemy_land_dir = -1  # направление наземного врага, при движении направо это 1, налево же -1 

enemy_land_anim_count = 0  # счетчик-индекс для изображений в списке анимаций наземного врага
enemy_land_x = 600  # координаты наземного врага по x
enemy_land_y = 500  # координаты наземного врага по y

# АНИМАЦИЯ И ДВИЖЕНИЕ ЛЕТАЮЩЕГО ВРАГА

enemy_sky_left = [
    img('enemy_sky_left/enemy_sky_left1.png'),
    img('enemy_sky_left/enemy_sky_left2.png'),
    img('enemy_sky_left/enemy_sky_left3.png'),
    img('enemy_sky_left/enemy_sky_left4.png'),
    img('enemy_sky_left/enemy_sky_left5.png'),
    img('enemy_sky_left/enemy_sky_left4.png'),
    img('enemy_sky_left/enemy_sky_left3.png'),
    img('enemy_sky_left/enemy_sky_left2.png')
] # список из подключенных картинок летающего врага, летящего налево
enemy_sky_right = [
    img('enemy_sky_right/enemy_sky_right1.png'),
    img('enemy_sky_right/enemy_sky_right2.png'),
    img('enemy_sky_right/enemy_sky_right3.png'),
    img('enemy_sky_right/enemy_sky_right4.png'),
    img('enemy_sky_right/enemy_sky_right5.png'),
    img('enemy_sky_right/enemy_sky_right4.png'),
    img('enemy_sky_right/enemy_sky_right3.png'),
    img('enemy_sky_right/enemy_sky_right2.png')
] # список из подключенных картинок летающего врага, летящего направо

# список из которого по значению enemy_sky_dir будет выбрана анимация
# первый элемент пуст так как enemy_sky_dir никогда не равна 0
enemy_sky_anim = [0, enemy_sky_right, enemy_sky_left]

enemy_sky_delay = 3  # количество кадров, через которое кадр анимации летающего врага сменяется
enemy_sky_delay_frame = 0  # количество кадров прошедших с момента последней смены кадра

enemy_sky_speed = 4  # это будем отнимать и прибавлять к координатам по х, тем самым регулируя скорость летающего врага
enemy_sky_dir = -1  # направление летающего врага, при движении направо это 1, налево же -1

enemy_sky_anim_count = 0  # счетчик-индекс для изображений в списке анимаций летающего врага
enemy_sky_x = 800  # координаты летающего врага по x
enemy_sky_y = 400  # координаты летающего врага по y

# БЭКГРАУНД
bg = img('pixel_bg.png')

bg_x = 0

# ВНЕДРЕНИЕ ВСЕГО В ИГРУ

running = True
while running:

    # НАСТРОЙКА БЭКГРАУНДА

    screen.blit(bg, (bg_x, 0))  # продолжаем бэкграунд вправо и влево
    screen.blit(bg, (bg_x + 1099, 0))
    screen.blit(bg, (bg_x - 1099, 0))

    bg_x -= 0  # настраиваем скорость движения бэкграунда (изначально статичен)
    if bg_x == -1099:
        bg_x = 0

    # ВЫВОД ЖИЗНЕЙ ИГРОКА

    font = pygame.font.SysFont(None, 24)  # инициализация шрифта
    lives_img = font.render(f'Жизни: {player_lives}', True, (0, 0, 0))  # рендер изображения
    screen.blit(lives_img, (20, 20))  # вывод изображения на экран

    # ВНЕДРЕНИЕ ВРАГОВ, НАСТРОЙКА ИХ АНИМАЦИИ И ИХ ДВИЖЕНИЕ

    # наземный враг ходит от одного края экрана к другому и обратно
    enemy_land_x += enemy_land_speed * enemy_land_dir
    if enemy_land_x not in range(0, 1099-104): enemy_land_dir = -enemy_land_dir

    # летающий враг летит от одного края экрана к другому и обратно
    enemy_sky_x += enemy_sky_speed * enemy_sky_dir
    if enemy_sky_x not in range(0, 1099-98): enemy_sky_dir = -enemy_sky_dir

    # наземный враг
    screen.blit(enemy_land_anim[enemy_land_dir][enemy_land_anim_count], (enemy_land_x, enemy_land_y))
    # летающий враг
    screen.blit(enemy_sky_anim[enemy_sky_dir][enemy_sky_anim_count], (enemy_sky_x, enemy_sky_y))

    # строчки ниже - настройка индексов анимаций наземного врага
    if enemy_land_delay_frame == enemy_land_delay:  # проверяем количество прошедших кадров, чтобы понять, пора ли сменять кадр
        enemy_land_delay_frame = 0
        if enemy_land_anim_count == 1:  # Обнуляем индекс, когда доходим до последнего элемента списка (чтобы не выйти за него)
            enemy_land_anim_count = 0
        else:
            enemy_land_anim_count += 1  # каждый раз, заходя в цикл, будем увеличивать индекс, выводя поочередно все элементы
    else:
        enemy_land_delay_frame += 1

    # строчки ниже - настройка индексов анимаций летающего врага
    if enemy_sky_delay_frame == enemy_sky_delay:  # проверяем количество прошедших кадров, чтобы понять, пора ли сменять кадр
        enemy_sky_delay_frame = 0
        if enemy_sky_anim_count == 7:  # Обнуляем индекс, когда доходим до последнего элемента списка (чтобы не выйти за него)
            enemy_sky_anim_count = 0
        else:
            enemy_sky_anim_count += 1  # каждый раз, заходя в цикл, будем увеличивать индекс, выводя поочередно все элементы
    else:
        enemy_sky_delay_frame += 1

    # ВНЕДРЕНИЕ ИГРОКА И НАСТРОЙКА ЕГО АНИМАЦИИ

    player = img('player_right/player_right1.png')  # базовая картинка игрока
    player_left = img('player_left/player_left1.png')  # картинка игрока повёрнутого влево
    keys = pygame.key.get_pressed()  # Кнопка, на которую сейчас нажимает пользователь
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    # Выводим на экран игрока с указанием его координат,
    # при этом выводя все элементы списка по индексу указанной в кв скобках переменной. Это для эффекта движения влево
        turn_left = True  # теперь игрок должен быть повёрнут влево
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_x:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
        # это то же самое, но для эффекта движения вправо
        turn_left = False  # теперь игрок больше не должен быть повёрнут влево
    elif turn_left:
        screen.blit(player_left, (player_x, player_y))  # делаем такую картинку после движения влево
    else:
        screen.blit(player, (player_x, player_y))  # делаем такую картинку когда игрок стоит
    # строчки ниже - настройка индексов анимаций игрока
    if player_delay_frame == player_delay:
        player_delay_frame = 0
        if player_anim_count == 1:  # Обнуляем индекс, когда доходим до последнего элемента списка (чтобы не выйти за него)
            player_anim_count = 0
        else:
            player_anim_count += 1  # каждый раз, заходя в цикл, будем увеличивать индекс, выводя поочередно все элементы
    else:
        player_delay_frame += 1

    # НАСТРОЙКА ДВИЖЕНИЯ И ПРЫЖКА ИГРОКА

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 20:
        # Если эта кнопка равна стрелке влево или букве A, да и коорд игр больше 50 (невидимая граница слева), то:
        player_x -= player_speed  # движемся влево, вычитая показатели из координат игрока
        if player_x <= frame_left:  # настраиваем движение рамки игрока и движение бэкграунда при нажатии "влево"
            frame_left -= player_speed
            frame_right -= player_speed
            bg_x += 3
            if bg_x == 1100:
                bg_x = 0
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < 1039:
        # Если эта кнопка равна стрелке вправо или букве D, да и коорд игр меньше 649 (невидимая граница справа), то:
        player_x += player_speed  # движемся вправо, прибавляя показатели к координатам игрока
        if player_x >= frame_right:  # настраиваем движение рамки игрока и движение бэкграунда при нажатии "вправо"
            frame_left += player_speed
            frame_right += player_speed
            bg_x -= 3
            if bg_x == -1100:
                bg_x = 0
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x <= 20:
        # Если эта кнопка равна стрелке влево или букве A, да и коорд игр больше 50 (невидимая граница слева), то:
        player_x -= 0  # движемся влево, вычитая показатели из координат игрока
        bg_x += 3
        if bg_x == 1101:
            bg_x = 0
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x >= 1039:
        # Если эта кнопка равна стрелке вправо или букве D, да и коорд игр меньше 649 (невидимая граница справа), то:
        player_x += 0  # движемся вправо, прибавляя показатели к координатам игрока
        bg_x -= 3
        if bg_x == -1101:
            bg_x = 0

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

    # ВЫЯВЛЕНИЕ КОЛЛИЗИЙ ВРАГОВ И ИГРОКА

    # создаем хитбоксы или репрезентации форм игрока и врагов в виде простых в обращении прямоугольников
    # для игрока и наземного врага хитбокс того же размера что и изображение,
    # но у летающего монстра в хитбокс входит только тело и хвост
    player_hitbox = Rect(player_x, player_y, 26, 34)
    enemy_land_hitbox = Rect(enemy_land_x, enemy_land_y, 104, 88)
    enemy_sky_hitbox = Rect(enemy_sky_x, enemy_sky_y + 49, 98, 44)

    # выявляем коллизии хитбоксов, то есть пересечения прямугольника игрока с прямогугольниками врагов
    collision = Rect.colliderect(player_hitbox, enemy_land_hitbox)
    collision = collision or Rect.colliderect(player_hitbox, enemy_sky_hitbox)

    # если выявлена коллизия, игрок теряет одну жизнь
    # режим неуязвимости длится 20 кадров, в течение которых игрок не получает урон
    # благодаря этому игрок не теряет все жизни, находясь в контакте с врагов лишь 5 кадров
    if collision and not invincible:
        player_lives -= 1
        invincible = 20

    # учитываем кадр как часть периода неуязвимости
    if invincible: invincible -= 1


    # СТРЕЛЬБА

    if bullets:
        for (i, el) in enumerate(bullets):
            screen.blit(bullet, (el.x, el.y))  # выводим элемент в текущих координатах
            if not turn_left:
                el.x += 15
            else:
                el.x -= 15

            if el.x > 1110 or el.x < -10:
                bullets.pop(i)  # за пределами экрана пуля убирается

            if el.colliderect(enemy_land_hitbox):  # при столкновении пули и монстра
                enemy_land_x = -500  # монстр помещается за пределы экрана
                bullets.pop(i)  # пуля убирается
            if el.colliderect(enemy_sky_hitbox):
                enemy_sky_x = -500
                bullets.pop(i)

    # если жизни кончаются игра завершается
    if player_lives == 0: running = False

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == KEYUP and event.key == pygame.K_b and bullets_left > 0:  # при отпускании клавиши B
            bullets_left -= 1  # уменьшается количество оставшихся пуль
            if not turn_left:
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))  # добавляем в список пулю
            else:
                bullets.append(bullet.get_rect(topleft=(player_x - 5, player_y + 10)))

    clock.tick(20)  # указываем количество фреймов за 1 сек, т.е. количество раз, которое проиграется цикл за 1 сек
    # иначе говоря, скорость смены изображений-анимаций игрока.
