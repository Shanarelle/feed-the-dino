import pygame
import os
import random

# custom events to keep track of candies and scores
NEWCANDY = pygame.USEREVENT + 1
DEADCANDY = pygame.USEREVENT + 2
BADCANDY = pygame.USEREVENT + 3

#load a single image for use with a sprite
def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()
	
# slice and image along its width so that you end up with a list of images in sequence
# - can be used for animations
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
    	# repeat to slow down the animation without needing extra images
    	images.append(master_image.subsurface((i*w,0,w,h)))
    	images.append(master_image.subsurface((i*w,0,w,h)))
    return images
	
	
# base class for candies that will post an event detailing its attributes when it falls off the bottom of the screen
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
		''' remove from groups if off screen '''
		if self.y >= pygame.display.get_surface().get_height():
			pygame.event.post(pygame.event.Event(DEADCANDY, xpos=self.x, speed=self.speed, kind=self.kind))
			self.kill()

# special class for candies that take away points
class BadCandy(Candy):
	def __init__(self, speed, ycoord):
		Candy.__init__(self, speed, ycoord)
		self.image, self.rect = load_image('badcandy.jpg')
		self.kind = 'badcandy'
		
			
class Dino(pygame.sprite.Sprite):
	#moves an dino along the bottom of the screen, 
	#following the mouse
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('data', 'normal.jpg')).convert()
		self.rect = self.image.get_rect()
		self.pos = pygame.display.get_surface().get_width() / 2
		self.previous_mouse = 0
		self.movement_speed = 5
		self.previous_direction = pygame.K_LEFT
		self.rect.bottom = pygame.display.get_surface().get_height()
		self.status = 0
		''' for animation '''
		self._delay = 1000 / 40
		self._last_update = 0
		self._frame = -1
		# the two possible animations
		self._images = load_sliced_sprites(72, 91, 'ready-lots.jpg')
		self._images2 = load_sliced_sprites(72, 91, 'eaten-lots.jpg')
	
	def update(self):
		''' move the dino along the bottom of the screen 
		    based on the mouse position '''
		pos = pygame.mouse.get_pos()
		screen = pygame.display.get_surface()
		if pos[0] != self.previous_mouse:
			self.pos = pos[0]
			self.previous_mouse = pos[0]
		''' move the dino along the bottom of the screen
			based on arrowkey presses '''
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.pos = self.pos - self.movement_speed
			# add in a certain amount of momentum - so you build up speed faster if you don't change directions
			if self.previous_direction == pygame.K_LEFT:
				self.movement_speed = self.movement_speed + 1
			else:	
				self.movement_speed = 5
			self.previous_direction = pygame.K_LEFT
		elif keys[pygame.K_RIGHT]:
			self.pos = self.pos + self.movement_speed
			if self.previous_direction == pygame.K_RIGHT:
				self.movement_speed = self.movement_speed + 1
			else:
				self.movement_speed = 5
			self.previous_direction = pygame.K_RIGHT
		if self.pos < (screen.get_width()-self.rect.width):
			self.rect.left = self.pos
		else:
			self.rect.right = screen.get_width()
		''' do some animation '''
		t = pygame.time.get_ticks()
		if self.status != 2:
			if t - self._last_update > self._delay:
				self._frame += 1
				self._last_update = t
				#run through opening mouth sequence
				if self.status == 1:
					if self._frame < len(self._images):
						self.image = self._images[self._frame]
						
				# run through eating sequence
				else:
					if self._frame < len(self._images2):
						self.image = self._images2[self._frame]
	
	# determine collisions between the dino and any candies - set off the relevant animation if any
	def ready(self, candylist, badcandylist):
		bigger = pygame.sprite.collide_rect_ratio(1.5)
		close_enough = pygame.sprite.spritecollide(self, candylist, False, bigger)
		close_enough.extend(pygame.sprite.spritecollide(self, badcandylist, False, bigger))
		collision = pygame.sprite.spritecollide(self, candylist, True)
		badcollision = pygame.sprite.spritecollide(self, badcandylist, True)
				
		if len(collision) > 0 or len(badcollision) > 0:	#eaten candy
			if self.status != 2:
				self.status = 2
				self._frame = -1
		elif len(close_enough) > 0:	#change image - will collide shortly
			if self.status != 1:
				self.status = 1
				self._frame = -1
		else:
			if self.status != 0:
				self.status = 0
				self.image = pygame.image.load(os.path.join('data', 'normal.jpg')).convert()
		return collision, badcollision
		
	
# display an explosion on the screen for 15 ticks		
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
			
# display a minus sign on the screen for 15 ticks to highlight to the player that they have lost a life
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
			