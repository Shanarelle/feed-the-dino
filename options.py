import pygame
import os

# handles all effects (and their options) such as sound and highscores

##constants
MISSEDCANDY = 0
LEVELUP = 1
LOSTLIFE = 2
BG_COLOUR = (224, 238, 238)
TEXT_COLOUR = (0,100,0)

#load all sound files
pygame.mixer.init()
missed_sound = pygame.mixer.Sound(os.path.join('data', 'candy-missed.wav'))
missed_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound(os.path.join('data', 'level-up.wav'))
level_up_sound.set_volume(0.2)
lost_life_sound = pygame.mixer.Sound(os.path.join('data', 'lost-life.wav'))
lost_life_sound.set_volume(0.2)
background_music = pygame.mixer.Sound(os.path.join('data', 'background-music.ogg'))
background_music.set_volume(0.05)

#set background music and sound effects on as default
soundeffects = True
music = False
#read the existing list of highscores
highscores = []
file = open(os.path.join('data', 'highscores.txt'), 'r')
line = file.readline()
interesting = line.strip('[]')
separate = interesting.split('(')
#iterate through the highscores in (name, score) format
for item in separate:
	if len(item) > 1:
		item = item.rstrip(')')
		parts = item.split(',')
		parts[1] = parts[1].strip(' \')\'')
		highscores.append((int(parts[0]), parts[1]))
file.close()
print 'highscores: ' + repr(highscores)

	
# utility functions to abstract away from the details of the background music
def playbackground():
	background_music.play(loops=-1)
	
def stopbackground():
	background_music.stop()
	
# switch between the background music being on or off
def toggle_background():
	global music
	if music:
		background_music.stop()
		music = False
	else:
		background_music.play(loops=-1)
		music = True
		
#increase the volume of all sounds by a small amount
def increase_volume():
	missed_sound.set_volume(missed_sound.get_volume() + 0.1)
	level_up_sound.set_volume(level_up_sound.get_volume() + 0.1)
	background_music.set_volume(background_music.get_volume() + 0.1)

#decrease the volume of all sounds by a small amount
def decrease_volume():
	missed_sound.set_volume(missed_sound.get_volume() - 0.1)
	level_up_sound.set_volume(level_up_sound.get_volume() - 0.1)
	background_music.set_volume(background_music.get_volume() - 0.1)

# switch between sound effects, such as losing a heart, being on or off
def toggle_effects():
	global soundeffects
	if soundeffects:
		soundeffects = False
	else:
		soundeffects = True

# plays the correct soundeffect based on the parameter passed in
def play_soundeffect(type):
	if soundeffects:
		if type == MISSEDCANDY:
			missed_sound.play()
		if type == LEVELUP:
			level_up_sound.play()
		if type == LOSTLIFE:
			lost_life_sound.play()
			
# adds a highscore to the correct placement on the highscores list - removes the lowest entry
# writes the highscores to the highscores file
def add_highscore(score, name):
	global highscores
	for item in highscores:
		if score > item[0]:
			highscores.insert(highscores.index(item), (score, name))
			highscores.pop() #removes the lowest score - list should always be 5 items long
			file = open(os.path.join('data', 'highscores.txt'), 'w')
			file.write(repr(highscores))
			file.close()
			break

# display the current list of highscores on the screen - 
# will effectively pause the game until dismissed
def show_highscores():
	global highscores
	screen = pygame.display.get_surface()
	typeset = pygame.font.Font(None, 20)
	y = screen.get_rect().centery
	x = screen.get_rect().centerx
	y -= 2*(typeset.get_linesize() + 2)
	bigfont = pygame.font.Font(None, 38)
	text = bigfont.render("HighScores", True, TEXT_COLOUR, BG_COLOUR)
	textRect = text.get_rect()
	textRect.centerx = x
	textRect.bottom = y - 5
	screen.blit(text, textRect)
	for item in highscores:
		text = typeset.render(str(item[1]) + '    ' + str(item[0]), True, TEXT_COLOUR, BG_COLOUR)
		textRect = text.get_rect()
		textRect.centerx = x
		textRect.top = y
		screen.blit(text, textRect)
		y += typeset.get_linesize() + 2
	
	pygame.display.flip()
	