import pygame
import os
import candy
import widgets
import random
import menuBar
import options

FLASH = pygame.USEREVENT + 5
# the height of the static menu bar
STATIC = 14

# display an initial prompt telling the user how to initialise the game
def display_play_prompt(extra_text=''):
	font = pygame.font.Font(None, 22)
	text = font.render('Press enter to play ' + extra_text, True, options.TEXT_COLOUR, options.BG_COLOUR)
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_height() - 50

	screen.blit(text, textRect)
	pygame.display.flip()

# display a letter in along the central horizontal axis of the screen
# used to display user input when entering their name for a highscore
def display_letter(letter, xpos, on=True):
	if on:
		text = font.render(letter, True, options.TEXT_COLOUR)
	else:
		text = font.render(letter, True, options.BG_COLOUR)
	textRect = text.get_rect()
	textRect.topleft = (xpos, screen.get_rect().centery+font.get_linesize())
	screen.blit(text, textRect)
	pygame.display.flip()

# controls the whole process of getting a user to input their name for a highscore.
# displays a flashing underscore after the last letter entered to indicate the 
# possibility of further letters being added
# will return name when enter is pressed
def get_name():
	clock = pygame.time.Clock()
	screen = pygame.display.get_surface()
	#typeset = pygame.font.Font(None, 40)
	text = font.render('Name: ', True, options.TEXT_COLOUR)
	textRect = text.get_rect()
	textRect.topright = (screen.get_rect().centerx, screen.get_rect().centery+font.get_linesize())
	screen.blit(text, textRect)
	# begin interactive part - waits for keyboard input
	# will flash underscore every 3 seconds
	flash = pygame.time.set_timer(FLASH, 200)
	x = screen.get_rect().centerx
	done = False
	on = False
	name = ''
	while done == False:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == FLASH: #blits an underscore as prompt, alternating visible and not visible
				display_letter('_', x, on)
				on = not on
			if event.type == pygame.KEYDOWN: #print the next character of the name and store it
				if event.key == pygame.K_RETURN:
					done = True
				elif event.key == pygame.K_BACKSPACE:
					name = name[:-1]
					x -= font.size(letter)[0]
					display_letter(letter, x, False)
				else:
					letter = pygame.key.name(event.key)
					if (len(letter) == 1):
						name = name + letter
						display_letter('_', x, False) #erase any current underscore
						display_letter(letter, x)
						x += font.size(letter)[0]
	return name	

# called when the number of lives = 0
# displays the users score then calls the functions to get their name 
# and add them to the highscores list
def end_game(score):
	screen.blit(background, (0, STATIC))
	text = font.render('Game Over', True, options.TEXT_COLOUR)
	textRect = text.get_rect()
	textRect.midbottom = (screen.get_rect().centerx, screen.get_rect().centery+font.get_linesize())
	screen.blit(text, textRect)
	font_small = pygame.font.Font(None, 24)
	text1 = font.render('Score: ' + repr(score), True, options.TEXT_COLOUR)
	text1Rect = text.get_rect()
	text1Rect.midbottom = (screen.get_rect().centerx, screen.get_rect().centery)
	screen.blit(text1, text1Rect)
	pygame.display.flip()
	#get name from them
	options.add_highscore(score, get_name())
	screen.blit(background, (0, STATIC))
	pygame.display.flip()


''' main game loop - not the outermost main loop so that the game can be quit by 
hitting the escape key
 '''
def play_game():
	global font

	#set up dino character
	character = candy.Dino()
	allsprites = pygame.sprite.RenderPlain((character))	#group
	clock = pygame.time.Clock()

	#set up widgets to go on screen - hearts atm
	hearts = widgets.Hearts(screen.get_width(), STATIC, 3)
	widget_list = pygame.sprite.RenderPlain(hearts)

	#set up menu
	sub_menu = menuBar.dropMenu('Sounds', (menuBar.menuItem('Toggle Background Music', options.toggle_background), menuBar.menuItem('Toggle Sound Effects', options.toggle_effects)))
	main_menu = menuBar.dropMenu('File', (menuBar.menuItem('Highscores', options.show_highscores), menuBar.menuItem('Up', options.increase_volume), menuBar.menuItem('Down', options.decrease_volume), sub_menu))
	bar = menuBar.menuBar(main_menu)
	allsprites.add(bar)

	#set up game tracking variables and sound effects
	candylist = pygame.sprite.RenderPlain()
	badlist = pygame.sprite.RenderPlain()
	cont = True
	score = 0
	misses = 0
	levelthreshold = 5
	level = 1
	lives = 3
	candyGen = pygame.time.set_timer(candy.NEWCANDY, 2000)
	badCandyGen = pygame.time.set_timer(candy.BADCANDY, 5000)

	# initialise a font module to display things to the screen
	font = pygame.font.Font(None, 42)
	text = font.render('Begin!!', True, options.TEXT_COLOUR, options.BG_COLOUR)
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery

	screen.blit(background, (0, STATIC))
	screen.blit(text, textRect)
	pygame.display.flip()
	pygame.time.wait(500)
	options.playbackground()

	# process events
	while cont: 
		clock.tick(30)
		screen.blit(background, (0, STATIC))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				cont = False
				options.stopbackground()
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				cont = False
				options.stopbackground()
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			# press p to pause
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				paused = True
				while paused:
					event = pygame.event.wait()
					if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
						paused = False
			elif event.type == candy.NEWCANDY:
				slow_bound = random.randrange(0, level)
				if slow_bound > 3:
					speed = random.randrange(3, 6)
				else:
					speed = random.randrange(1, 6)
				candylist.add(candy.Candy(speed, STATIC))
			elif event.type == candy.BADCANDY:
				badlist.add(candy.BadCandy(random.randrange(1, 6), STATIC))
			elif event.type == candy.DEADCANDY:
				misses += 1
				# some penalties for a miss based on current level
				# if level is above 5 then missing a slow candy deducts a point
				if event.kind == 'badcandy':
					pass
				else:
					if level > 5 and event.speed < 3:
						score -= 1
						allsprites.add(candy.Minus(event.xpos))
					
					allsprites.add(candy.Explosion(event.xpos))	
					options.play_soundeffect(options.MISSEDCANDY)
				pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))
		#update all game objects
		allsprites.update()
		candylist.update()
		badlist.update()
		widget_list.update()
		#print allsprites
		if len(candylist) > 0:
			result, badresult = character.ready(candylist, badlist)
			if len(result) > 0:	#THERE WAS A COLLISION
				score += 1
			if len(badresult) > 0: #ate a bad candy
				lives -= 1
				hearts.minus_heart()
				options.play_soundeffect(options.LOSTLIFE)
			pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))		
		# draw the new versions of all game objects to the screen
		allsprites.draw(screen)
		candylist.draw(screen)
		badlist.draw(screen)
		widget_list.draw(screen)
		pygame.display.flip()
		
		# if the score is sufficient, advance to the next level and display some congratulatory text
		if score >= levelthreshold:
			levelthreshold = levelthreshold * 3
			level += 1
			# add an extra candy generator every 2 levels
			if level % 2 == 0:
				candyGen = pygame.time.set_timer(candy.NEWCANDY, 2000/level)
			if level % 5 == 0:
				badCandyGen = pygame.time.set_timer(candy.BADCANDY, 5000/level)
			pygame.display.set_caption('Raining Candy      Level: ' + repr(level) + ',  Score: ' + repr(score) + ', Candies missed: ' + repr(misses) + ', Lives:' + repr(lives))
			options.play_soundeffect(options.LEVELUP)
			text = font.render('Level Up!', True, (0, 0, 255))
			textRect = text.get_rect()
			textRect.centerx = screen.get_rect().centerx
			textRect.centery = screen.get_rect().centery
			screen.blit(text, textRect)
			pygame.display.flip()
			pygame.time.wait(800)
			
		if lives < 1 and cont:
			cont = False
			end_game(score)
			


pygame.init()
#options.init()
menuBar.init()
screen = pygame.display.set_mode((760, 480))
pygame.display.set_caption('Raining Candy')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size()).convert()
background.fill(options.BG_COLOUR)
screen.blit(background, (0, 0))
pygame.display.flip()

cont = True
display_play_prompt()

while cont:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			cont = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			options.stopbackground()
			cont = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			play_game()
			options.show_highscores()
			display_play_prompt("again")

