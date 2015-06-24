import pygame
import sys
import random

''' This will create a pygame screen with 10 initial dinos.
	Press the up arrow to add another dino.
	Click an dino to remove it.
	Enjoy the sight of many dinos.
 '''


''' 
 will put a bunch of dinos in random (unoccupied) places
'''
def init_dinos(occupied, numberOfChars):
	for i in range(numberOfChars):
		character = pygame.image.load('dino_small.jpg').convert()	# load the image
		loc = fresh(character.get_width(), character.get_height())	# determine where to place it
		if loc != None:
			occupied.append(loc)							# add it to the list of occupied rects
			screen.blit(character, loc)								# put it on the screen

	pygame.display.update()										# make it actually display
	return occupied											# make caller aware of changes in the occupation list

def erase_dino(loc):
	for i in range(len(occupied)):
		if occupied[i].collidepoint(loc) == True:
			print "erasing a dino"
			screen.fill((159, 182, 205), occupied[i])
			pygame.display.update(occupied[i])
			occupied.pop(i)
			break
	
''' 
 will generate the x,y coordinates of the top left of a box
 of the designated size that is free
 will return None if no such box exists
'''
def fresh(width, height):
	i = 0													# a counter to make sure not stuck here infinitely
	while True:
		x = random.randrange((screen.get_width() - width)/10) * 10
		y = random.randrange((screen.get_height() - height)/10) * 10
		box = pygame.Rect(x, y, width, height)
		i = i + 1
		if box.collidelist(occupied) == -1:
			return box
		if i>40:
			return None


def draw_dino(location):		#location should be a tuple
	occupied.append(location)
	character = pygame.image.load('dino.jpg').convert()
	screen.blit(character, location)
	pygame.display.update()
	
	
#do the game space setup
pygame.init()
# create a window surface of the appropriate size
screen = pygame.display.set_mode((500, 450))
pygame.display.set_caption("He's hungry!")
screen.fill((159, 182, 205))


#create an empty list that will hold all occupied rectangles in (designation, placement) pairs
occupied = []
														
occupied = init_dinos(occupied, 10);							# list tracks where there are things on the screen...
																# number says how many dinos to start with

#enter the main loop of the game that will accept inputs
while True:
	for event in pygame.event.get():
		# allows you to quit
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			erase_dino(event.pos)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			draw_dino(fresh(80,80))
			
			