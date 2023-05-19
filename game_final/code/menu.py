import pygame
from settings import *

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


# Эта функция упрощает загрузку изображений
def img(filename):
    return pygame.image.load(f'../graphics/screens/{filename}')

# РАБОТА С ТЕКСТОМ


def print_text(message, x, y, font_color=(255, 255, 255), font_type="../graphics/fonts/Sonic Filled.ttf", font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# ДЕЛАЕМ КНОПКИ ДЛЯ МЕНЮ

starting = False  # пригодится для отслеживания нажатия на кнопку play в меню
read = False  # прочитаны ли инструкции управления


class Button:

    def __init__(self, width, height):  # настраиваем длину, ширину и цвета
        self.width = width
        self.height = height
        self.inactive_color = (36, 36, 36)  # если не наводим мышью на кнопку
        self.active_color = (69, 69, 69)  # если наводим мышью на кнопку

    def draw(self, x, y, message, action=None, font_size=30):  # делаем собственно кнопку
        global starting
        global read
        mouse = pygame.mouse.get_pos()  # отслеживаем позицию мыши
        click = pygame.mouse.get_pressed()  # узнаем, нажал ли пользователь на кнопку мыши

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:  # если курсор находится на кнопке по у и х
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))  # на второй позиции цвет

            if click[0] == 1:  # это значит, что произошло нажатие левой кнопкой мыши
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
                if message == "Play":  # если произошло нажатие на кнопку с такой надписью, то глоб перемен истин
                    starting = True
                if message == 'Ok':
                    read = True
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


# ФУНКЦИЯ ДЛЯ ПРОРИСОВКИ ИГРОВОГО МЕНЮ

def menu():
    global starting
    global read
    menu_bg = img('menu.jpg')  # загружаем фото заднего фона меню

    start_button = Button(148, 79)
    quit_button = Button(148, 79)

    show = True

    while show:  # пока показываем меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))  # от левого верхнего экрана прорисовать изображение, прорисовываем дисплей
        start_button.draw(526, 250, 'Play', None, 35)  # указываем координаты кнопки, на посл месте размер шрифта
        quit_button.draw(526, 400, "Quit", quit, 35)

        pygame.display.update()
        clock.tick(60)

        if starting:  # если пользователь нажал на кнопку play, то переменная истинна, а значит, меню исчезает
            break

    controls = img('controls.png')  # загружаем картинку с инструкциями по управлению

    ok_button = Button(84, 64)

    read = False

    while not read:  # пока показываем меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))  # от левого верхнего экрана прорисовать изображение, прорисовываем дисплей
        screen.blit(controls, (0, 0))
        ok_button.draw(555, 433, 'Ok', None, 30)  # указываем координаты кнопки, на посл месте размер шрифта

        pygame.display.update()
        clock.tick(60)
