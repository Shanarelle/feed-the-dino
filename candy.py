import pygame
import os
import random

def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()
	
	
class Candy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('fist.bmp')
		screen = pygame.display.get_surface()
		self.x = random.randrange(screen.get_width() - self.rect.width)
		#print self.x
		self.y = 0
		#print self.y
		#self.rect.topleft = self.x, self.y
	
	def update(self):
		''' move the candy down the screen slightly '''
		self.y = self.y + 1
		self.rect.topleft = self.x, self.y
		''' remove from groups if dead '''
		if self.y >= pygame.display.get_surface().get_height():
			self.kill()
			
			
class Omnom(pygame.sprite.Sprite):
	#moves an omnom along the bottom of the screen, 
	#following the mouse
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('omnom.jpg').convert()
		self.rect = self.image.get_rect()
		self.rect.bottom = pygame.display.get_surface().get_height()
		self.status = 0
	
	def update(self):
		''' move the omnom based on the mouse position '''
		pos = pygame.mouse.get_pos()
		screen = pygame.display.get_surface()
		if pos[0] < (screen.get_width()-self.rect.width):
			self.rect.left = pos[0]
		else:
			self.rect.right = screen.get_width()
	
	def ready(self, candylist):
		bigger = pygame.sprite.collide_rect_ratio(1.5)
		close_enough = pygame.sprite.spritecollide(self, candylist, False, bigger)
		if len(close_enough) > 0:	#change image
			if self.status != 1:
				self.status = 1
				self.image = pygame.image.load('omnom-ready.jpg').convert()
			collision = pygame.sprite.spritecollide(self, candylist, True)
			if len(collision) > 0:	#eaten candy
				self.status = 2
				self.image = pygame.image.load('omnom-eaten.jpg').convert()
			return collision
		else:
			return []
			
			