import pygame
import os
import random

NEWCANDY = pygame.USEREVENT + 1
DEADCANDY = pygame.USEREVENT + 2
BADCANDY = pygame.USEREVENT + 3

def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()
	
def load_sliced_sprites(w, h, filename):
    '''
	from shinylittlething.com
    Specs :
    	Master can be any height.
    	Sprites frames width must be the same width
    	Master width must be len(frames)*frame.width
    Assuming your resources directory is named "data"
    '''
    images = []
    master_image = pygame.image.load(os.path.join('data', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width/w)):
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images
	
	
class Candy(pygame.sprite.Sprite):
	def __init__(self, speed, ycoord):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('candy.jpg')
		screen = pygame.display.get_surface()
		self.x = random.randrange(screen.get_width() - self.rect.width)
		#print self.x
		self.y = ycoord
		self.speed = speed
		self.kind = 'candy'
		#print self.y
		#self.rect.topleft = self.x, self.y
	
	def update(self):
		''' move the candy down the screen slightly '''
		self.y = self.y + self.speed
		self.rect.topleft = self.x, self.y
		''' remove from groups if dead '''
		if self.y >= pygame.display.get_surface().get_height():
			pygame.event.post(pygame.event.Event(DEADCANDY, xpos=self.x, speed=self.speed, kind=self.kind))
			self.kill()

class BadCandy(Candy):
	def __init__(self, speed, ycoord):
		Candy.__init__(self, speed, ycoord)
		self.image, self.rect = load_image('badcandy.jpg')
		self.kind = 'badcandy'
		
			
class Omnom(pygame.sprite.Sprite):
	#moves an omnom along the bottom of the screen, 
	#following the mouse
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('omnom.jpg').convert()
		self.rect = self.image.get_rect()
		self.rect.bottom = pygame.display.get_surface().get_height()
		self.status = 0
		''' for animation '''
		self._delay = 1000 / 40
		self._last_update = 0
		self._frame = -1
		# the two possible animations
		self._images = load_sliced_sprites(75, 70, 'omnom-opening.jpg')
		self._images2 = load_sliced_sprites(75, 70, 'omnom-nommin.jpg')
	
	def update(self):
		''' move the omnom along the bottom of the screen 
		    based on the mouse position '''
		pos = pygame.mouse.get_pos()
		screen = pygame.display.get_surface()
		if pos[0] < (screen.get_width()-self.rect.width):
			self.rect.left = pos[0]
		else:
			self.rect.right = screen.get_width()
		''' do some animation '''
		t = pygame.time.get_ticks()
		if self.status != 0:
			if t - self._last_update > self._delay:
				self._frame += 1
				#run through opening mouth sequence
				if self.status == 1:
					if self._frame < len(self._images):
						self.image = self._images[self._frame]
						self._last_update = t
						'''
					else:	#gone through a single round of animation
						self._frame = -1
						self.status = 0
						self.image = pygame.image.load('omnom.jpg').convert()
						'''
				# run through closing mouth sequence
				else:
					if self._frame < len(self._images2):
						self.image = self._images2[self._frame]
						self._last_update = t
					else:	#gone through a single round of animation
						self._frame = -1
						self.status = 0
						self.image = pygame.image.load('omnom.jpg').convert()
	
	
	def ready(self, candylist):
		bigger = pygame.sprite.collide_rect_ratio(1.5)
		close_enough = pygame.sprite.spritecollide(self, candylist, False, bigger)
		if len(close_enough) > 0:	#change image
			if self.status != 1:
				self.status = 1
				self._frame = -1
			collision = pygame.sprite.spritecollide(self, candylist, True)
			if len(collision) > 0:	#eaten candy
				self.status = 2
				self._frame = -1
			return collision
		else:
			if self.status != 0:
				self.status = 0
				self.image = pygame.image.load('omnom.jpg').convert()
			return []
		
			
class Explosion(pygame.sprite.Sprite):
	def __init__(self, xpos):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('explosion.jpg')
		screen = pygame.display.get_surface()
		self.x = xpos
		self.rect.bottomleft = (self.x, screen.get_height())
		self.ticker = 0
	
	def update(self):
		self.ticker += 1
		if self.ticker > 15:
			self.kill()
			
			
class Minus(pygame.sprite.Sprite):
	def __init__(self, xpos):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('minus.jpg')
		screen = pygame.display.get_surface()
		if xpos > 20:
			self.x = xpos
		else:
			self.x = 20
		self.rect.midbottom = (self.x, screen.get_height()-40)
		self.ticker = 0
	
	def update(self):
		self.ticker += 1
		if self.ticker > 15:
			self.kill()
			