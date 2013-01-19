'''
update method will be called every round of game loop.
if the mouse is within the menu area then don't return 
until it leaves.
drop down menu will appear when its representative is clicked on.
most clicks will just call a function implemented in the main game
module.

doesn't actually work for two levels of subbing, but does fine for 1
(can have 1 nested sub-menu in drop-down)
probably can't do multiple buttons on the menubar either
'''
import pygame
import options

FONT_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (200, 200, 200)

def init():
	pygame.font.init()
	
def donothing():
	print "I am a lie!"

class menuBar(pygame.sprite.Sprite):
	def __init__(self, menulist):
		pygame.sprite.Sprite.__init__(self)
		self.menulist = []
		self.menulist.append(menulist)
		self.rectlist = []				#so can figure out which button was clicked
		self.clickedlist = []
		self.font = pygame.font.Font(None, 20)
		screen = pygame.display.get_surface()
		size = screen.get_width(), self.font.get_linesize()
		self.image = pygame.Surface((size))
		background = self.image.copy()
		background.fill(BACKGROUND_COLOUR)
		self.rect = pygame.Rect((0,0), (size))
		screen.blit(background, self.rect)
		self.image.set_alpha(0)		#make it invisible
		x = 0
		for item in self.menulist:
			text = self.font.render(menulist.label, True, FONT_COLOUR, BACKGROUND_COLOUR)
			textRect = text.get_rect()
			textRect.topleft = (x,0)
			self.rectlist.append(textRect)
			screen.blit(text, textRect)
			x += textRect.width+6
	
	def update(self):
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):	#hovering within menu system
			pygame.mouse.set_visible(True)
		
		active = None
		active_rect = None
		while self.rect.collidepoint(pos) or active != None:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.rect.collidepoint(pos):
						for index in range(len(self.rectlist)):
							if self.rectlist[index].collidepoint(event.pos):
								print "Clicked file"
								active_rect = self.menulist[index].render(0,self.font.get_linesize())
								active = index
					elif active_rect.collidepoint(pos):
						new_rect = self.menulist[active].clicked(pygame.mouse.get_pos())
						print repr(new_rect) + 'new rect'
						print repr(active_rect)
						if new_rect != None:
							active_rect = active_rect.union(new_rect)
						print repr(active_rect) + 'after union'
					else:
						active = None
						active_rect = None
						for item in self.menulist:
							if item.rendered:
								item.derender()
			pos = pygame.mouse.get_pos()
		pygame.mouse.set_visible(False)
			
class menuItem():
	def __init__(self, name, function=donothing):
		self.label = name
		self.function = function
		self.rendered = True
		
	def clicked(self, coords):
		print repr(self.label) + ' clicked'
		self.function()
		return pygame.Rect(coords, (0,0))
		
	def render(self, xcoord, ycoord):
		return self.clicked((xcoord, ycoord))	#just so actual structure of menu not important to know
		#return pygame.Rect((xcoord, ycoord), (0,0))
		
	# does nothing because these are always classed as rendered
	def derender(self):
		pass
		
		
class dropMenu():
	def __init__(self, name, componentlist):
		self.label = name
		self.items = componentlist
		self.font = pygame.font.Font(None, 20)
		self.height = self.font.get_linesize()*len(self.items)
		self.width = 15
		self.y = 0
		self.rendered = False
		for item in self.items:
			size_test = self.font.size(item.label)
			if size_test[0] > self.width:
				self.width = size_test[0]
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(BACKGROUND_COLOUR)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
	
	# xcoord and ycoord should be the upper left corner of the menu
	def render(self, xcoord, ycoord):
		if not self.rendered:
			self.rendered = True
			self.rect.topleft = (xcoord, ycoord)
			screen = pygame.display.get_surface()
			screen.blit(self.image, (xcoord, ycoord))
			self.x = xcoord
			self.y = ycoord
			curr_y = ycoord
			for item in self.items:
				text = self.font.render(item.label, True, FONT_COLOUR, BACKGROUND_COLOUR)
				textRect = text.get_rect()
				textRect.topleft = (xcoord, curr_y)
				screen.blit(text, textRect)
				curr_y += self.font.get_linesize()
			pygame.display.flip()
			print repr(self.rect.right) + 'rect right'
			return self.rect
		else:		#this shouldn't be necessary
			return self.clicked((xcoord, ycoord))
		
	def clicked(self, coords):
		curr_y = coords[1]
		curr_y -= self.rect.top
		#print repr(self.rect.right) + 'rect right & x-coord ' + repr(coords[0]) + repr(self.label)
		if coords[0] < self.rect.right:
			print 'Some item clicked' + repr(self.label)
			guess = 0
			for index in range(len(self.items)):
				guess += self.font.get_linesize()
				if guess > curr_y:
					new_rect = self.items[index].render(self.x+self.width, guess)		#only works because menu same lineheight as this
					return new_rect
		else:	#must have clicked a submenu
			for item in self.items:
				if item.rendered:
					item.clicked(coords)
				
	def derender(self):
		self.rendered = False
		for item in self.items:
			if item.rendered:
				item.derender()
					
		
		
		
		
		