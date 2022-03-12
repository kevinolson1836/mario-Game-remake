from turtle import width
import pygame

class SpriteSheet():
	def __init__(self, image, width, height, scale, color, start, end):
		self.sheet = image
		self.width = width
		self.height = height
		self.scale = scale
		self.color = color
		self.start = start
		self.end = end

	def get_image(self, frame, width, height, scale, color, start, end):
		image = pygame.Surface((self.width, self.height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * self.width), self.end, self.width, self.height))
		image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
		image.set_colorkey(color)

		return image

	def get_scale(self):
		return(self.scale)

	def animate(self, frame):
		return(self.get_image(frame, self.width, self.height, self.scale, self.color, self.start, self.end))