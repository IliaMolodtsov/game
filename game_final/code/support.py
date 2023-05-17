from os import walk
import pygame


def import_folder(path):
    surface_list = []  # список, в котором будут все изображения из папки

    for _, __, img_files in walk(path):  # внутри walk работаем с изображениями, которые есть в папке
        for image in img_files:
            full_path = path + '/' + image  # определяем путь до изображения
            image_surf = pygame.image.load(full_path).convert_alpha()  # загружаем изображение
            surface_list.append(image_surf)  # добавляем изображение в список

    return surface_list
