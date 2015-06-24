import pygame 
import os

#utility functions that could be re-used for other games


#load an image from a file and return the image (converted for sprite use) and its bounding box
def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()


# a heart class that loads a heart image at a given set of coordinates and accepts
# a kill command that will cause it to destroy itself and disappear
# (used to give feedback to the user)
class Single_Heart(pygame.sprite.Sprite):
	def __init__(self, xcoord, ycoord):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('heart.png')
		self.rect.topleft = xcoord, ycoord

	def update(self):
		pass

	def destroy_heart(self):
		self.kill()

# a wrapper around the heart class that takes care of which specific heart to remove -
# accepts an initial number of hearts (with a set of coordinates for the right-most heart)
# and allows you to add or remove a heart at a time
class Hearts(pygame.sprite.RenderUpdates):
	def __init__(self, xcoord, ycoord, number):
		pygame.sprite.Group.__init__(self)
		self.xcoord = xcoord
		self.heart_list = []
		for i in range(number):
			self.xcoord = self.xcoord-30
			heart = Single_Heart(self.xcoord, ycoord)
			self.add(heart)
			self.heart_list.append(heart)

	def minus_heart(self):
		self.heart_list.pop().destroy_heart()
	
	def add_heart(self):
		self.xcoord = self.xcoord-30
		self.add(Single_Heart(self.xcoord, ycoord))