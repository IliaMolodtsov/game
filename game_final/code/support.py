import pygame
from os import walk
from csv import reader
from settings import tile_size


def import_folder(path):  # функция для импорта папок с изображениями врагов
    surface_list = []  # список, в котором будут все изображения из папки

    for _, __, image_files in walk(path):  # внутри walk работаем с изображениями, которые есть в папке
        for image in image_files:
            full_path = path + '/' + image  # определяем путь до изображения
            image_surf = pygame.image.load(full_path).convert_alpha()  # загружаем изображение
            surface_list.append(image_surf)  # добавляем изображение в список

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):  # функция для разрезки тайлов на отдельные части
    surface = pygame.image.load(path).convert_alpha()
    # импортируем графические материлы, чтобы поставить их на поверхность
    tile_num_x = int(surface.get_size()[0] / tile_size)  # получить количество тайлов в импортированных материалах
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)  # поверхность 64*64 пикселей
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

