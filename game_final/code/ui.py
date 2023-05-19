import pygame


class UI:  # интерфейс пользователя
    def __init__(self, surface):

        # setup
        self.display_surface = surface

        # жизни
        self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()  # загружаем фотку сердечка
        self.health_bar_topleft = (54, 39)  # координаты линии жизни
        self.bar_max_width = 152
        self.bar_height = 4

        # монеты
        self.coin = pygame.image.load('../ui/coin.png').convert_alpha()  # загружаем фотку монеты
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))  # топ лефт - координаты центра картинки
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf', 30)

    def show_health(self, current, full):  # функция для вывода жизней
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full  # сколько здоровья (жизни) сейчас
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, change_coins):  # функци для вывода монет
        self.display_surface.blit(self.coin, self.coin_rect)  # пишем, сколько монет будет
        coin_amount_surf = self.font.render(str(change_coins), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
