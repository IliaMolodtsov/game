from settings import screen_width, screen_height
import pygame


class Forest:
	def __init__(self):
		# загружаем слои
		self.layers = [f'../graphics/background/plx-{i+1}.png' for i in range(5)]
		self.layers = [pygame.image.load(i).convert_alpha() for i in self.layers]

		# растягиваем по размеру экрана
		self.layers = [pygame.transform.scale(i, (screen_width, screen_height)) for i in self.layers]

		# сдвиг для каждого слоя
		self.offset = [0] * 5

		# счетчики для разной скорости смещения слоев
		self.offset_timer = [0] * 5

	# обновляем сдвиг слоев
	def update(self, shift):
		if shift < 0:
			direct = -1
		else:
			direct = 1
		self.offset_timer = [i + shift * direct for i in self.offset_timer] 
		for i in range(5):
			while self.offset_timer[i] >= 5 - i:
				self.offset_timer[i] -= 5 - i
				self.offset[i] += 1 * direct
				if self.offset[i] <= -screen_width:
					self.offset[i] += screen_width
				if self.offset[i] >= screen_width:
					self.offset[i] -= screen_width

	# рисуем слои
	def draw(self, surface):
		for i in range(5):
			surface.blit(self.layers[i], (self.offset[i] - screen_width, 0))
			surface.blit(self.layers[i], (self.offset[i], 0))
			surface.blit(self.layers[i], (screen_width + self.offset[i], 0))
