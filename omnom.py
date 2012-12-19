import pygame
import sys
import random

''' defines some constants '''
#NORMAL = 0
#READY = 1
#EATEN = 2

class Omnom(pygame.sprite.Sprite):
	#moves an omnom along the bottom of the screen, 
	#following the mouse
	
	def _init_(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('omnom.jpg').convert()
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 70
		self.status = 0
	
	def update(self):
		''' move the omnom based on the mouse position '''
		pos = pygame.mouse.get_pos()
		self.rect.x = 80
	
	def ready(self, candylist):
		readybox = self.rect.inflate(15, 15)
		close_enough = readybox.collidelist(candylist)
		if close_enough != -1:	#change image
			if self.status != 1:
				self.status = 1
				self.image, self.rect = load_image('omnom-ready.jpg', -1)
			collision = readybox.collidelist(candylist)
			if collision != -1:	#eaten candy
				self.status = 2
				self.image, self.rect = load_image('omnom-eaten.jpg', -1)
			return collision
		else:
			return -1
			
			
			
			
			
			
			