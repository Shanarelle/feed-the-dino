import pygame
import os

MISSEDCANDY = 0
LEVELUP = 1

pygame.mixer.init()
missed_sound = pygame.mixer.Sound(os.path.join('data', 'candy-missed.wav'))
missed_sound.set_volume(0.1)
level_up_sound = pygame.mixer.Sound(os.path.join('data', 'level-up.wav'))
level_up_sound.set_volume(0.1)
background_music = pygame.mixer.Sound(os.path.join('data', 'background-music.ogg'))
background_music.set_volume(0.05)
soundeffects = True
music = True
	
def playbackground():
	background_music.play(loops=-1)
	
def stopbackground():
	background_music.stop()
	
def toggle_background():
	global music
	if music:
		background_music.stop()
		music = False
	else:
		background_music.play(loops=-1)
		music = True
		
def increase_volume():
	missed_sound.set_volume(missed_sound.get_volume() + 0.1)
	level_up_sound.set_volume(level_up_sound.get_volume() + 0.1)
	background_music.set_volume(background_music.get_volume() + 0.1)

def decrease_volume():
	missed_sound.set_volume(missed_sound.get_volume() - 0.1)
	level_up_sound.set_volume(level_up_sound.get_volume() - 0.1)
	background_music.set_volume(background_music.get_volume() - 0.1)

def toggle_effects():
	global soundeffects
	if soundeffects:
		soundeffects = False
	else:
		soundeffects = True

def play_soundeffect(type):
	if soundeffects:
		if type == MISSEDCANDY:
			missed_sound.play()
		if type == LEVELUP:
			level_up_sound.play()