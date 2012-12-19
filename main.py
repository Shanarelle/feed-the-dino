import pygame
import candy



pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption('Raining Candy      0')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size()).convert()
background.fill((250, 250, 250))
screen.blit(background, (0, 0))
pygame.display.flip()

character = candy.Omnom()
allsprites = pygame.sprite.RenderPlain((character))	#group
clock = pygame.time.Clock()

candylist = pygame.sprite.RenderPlain()
cont = True
round = 0
score = 0

while cont:
	clock.tick(30)
	round += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			cont = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			cont = False
	allsprites.update()
	print allsprites
	if round % 100 == 0:
		#candy = candy.Candy()
		candylist.add(candy.Candy())
		allsprites.add(candylist)
	if len(candylist) > 0:
		result = character.ready(candylist)
		# should do an action if this was true - start a timer
		if len(result) > 0:	#THERE WAS A COLLISION
			score += 1
			pygame.display.set_caption('Raining Candy     ' + repr(score))
	screen.blit(background, (0, 0))
	allsprites.draw(screen)
	pygame.display.flip()
		
		
		