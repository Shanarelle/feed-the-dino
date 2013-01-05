import pygame
import MenuSystem
import os
import candy
import random

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((560, 320))
pygame.display.set_caption('Raining Candy')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size()).convert()
background.fill((250, 250, 250))
screen.blit(background, (0, 0))
pygame.display.flip()

'''
#set up menu
MenuSystem.init()
# create the menus and submenus
sound_options = MenuSystem.Menu('Sounds', ('Toggle Background Music', 'Toggle Sound Effects'))
main_menu = MenuSystem.Menu('Menu', ('Options')) #'New Game    (F4)', 'Pause    (p)', 'High Scores', 'Quit'))
bar = MenuSystem.MenuBar()
bar.set((main_menu))
static = bar.lineheigth
pygame.display.update(bar)
ms = MenuSystem.MenuSystem()
'''
static = 14

#set up omnom character
character = candy.Omnom()
allsprites = pygame.sprite.RenderPlain((character))	#group
clock = pygame.time.Clock()

#set up game tracking variables and sound effects
candylist = pygame.sprite.RenderPlain()
badlist = pygame.sprite.RenderPlain()
cont = True
score = 0
misses = 0
missed_sound = pygame.mixer.Sound(os.path.join('data', 'candy-missed.wav'))
level_up_sound = pygame.mixer.Sound(os.path.join('data', 'level-up.wav'))
level_up_sound.set_volume(0.1)
background_music = pygame.mixer.Sound(os.path.join('data', 'background-music.ogg'))
background_music.set_volume(0.05)
levelthreshold = 5
level = 1
lives = 3
candyGen = pygame.time.set_timer(candy.NEWCANDY, 1000)
badCandyGen = pygame.time.set_timer(candy.BADCANDY, 5000)

# initialise a font module to display things to the screen
font = pygame.font.Font(None, 42)
text = font.render('Begin!!', True, (0,0,255), (255,255,255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery

screen.blit(text, textRect)
pygame.display.flip()
pygame.time.wait(500)
background_music.play(loops=-1)

'''
ev = event.wait()
pygame.display.update(bar.update(ev))
if bar.choice:
	print(bar.choice)
	print(bar.choice_label)
	print(bar.choice_index)
pygame.display.flip()
'''

while cont: 
	clock.tick(30)
	screen.blit(background, (0, static))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			cont = False
			background_music.stop()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			cont = False
			background_music.stop()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
			paused = True
			while paused:
				event = pygame.event.wait()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
					paused = False
		elif event.type == candy.NEWCANDY:
			candylist.add(candy.Candy(random.randrange(1, 6), static))
		elif event.type == candy.BADCANDY:
			badlist.add(candy.BadCandy(random.randrange(1, 6), static))
		elif event.type == candy.DEADCANDY:
			misses += 1
			# some penalties for a miss based on current level
			# if level is above 5 then missing a slow candy deducts a point
			if event.kind == 'badcandy':
				pass
			else:
				if level > 1 and event.speed < 3:
					score -= 1
					allsprites.add(candy.Minus(event.xpos))
				
				allsprites.add(candy.Explosion(event.xpos))	
				missed_sound.play()
			pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))
		'''else:	# will only accept mouse motion events
			if ms:
				pygame.display.update(ms.update(event))
				if ms.choice:
					print(ms.choice)
					print(ms.choice_label)
					print(ms.choice_index)
			#else:
			pygame.display.update(bar.update(event))
			if bar.choice:
				print(bar.choice)
				print(bar.choice_label)
				print(bar.choice_index)
	#bar.draw()	'''
	allsprites.update()
	candylist.update()
	badlist.update()
	#print allsprites
	if len(candylist) > 0:
		result = character.ready(candylist)
		badresult = character.ready(badlist)
		if len(result) > 0:	#THERE WAS A COLLISION
			score += 1
		if len(badresult) > 0:
			lives -= 1
		pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))		
	allsprites.draw(screen)
	candylist.draw(screen)
	badlist.draw(screen)
	pygame.display.flip()
	
	# if the score is sufficient, advance to the next level and display some congratulatory text
	if score >= levelthreshold:
		levelthreshold = levelthreshold * 3
		level += 1
		pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))
		level_up_sound.play()
		text = font.render('Level Up!', True, (0, 0, 255))
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = screen.get_rect().centery
		screen.blit(text, textRect)
		pygame.display.flip()
		pygame.time.wait(800)
		
	if lives < 1:
		screen.blit(background, (0, static))
		text = font.render('Game Over', True, (0, 0, 255))
		textRect = text.get_rect()
		textRect.midbottom = (screen.get_rect().centerx, screen.get_rect().centery+2)
		screen.blit(text, textRect)
		font_small = pygame.font.Font(None, 24)
		text1 = font.render('Score: ' + repr(score), True, (0, 0, 255))
		text1Rect = text.get_rect()
		text1Rect.midtop = (screen.get_rect().centerx, screen.get_rect().centery-2)
		screen.blit(text1, text1Rect)
		pygame.display.flip()
		pygame.time.wait(800)
		pygame.event.post(pygame.event.Event(pygame.QUIT))

		
		
		