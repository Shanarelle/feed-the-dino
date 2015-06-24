from Tkinter import *
import tkFileDialog
import sys
import main

def reset():
	print 'reset'
	
def pause_game():
	print 'pause game'
	
def show_scores():
	print 'show scores'
	
def toggle_music():
	print 'toggle music'
	
def toggle_sounds():
	print 'toggle sounds'



screen = Tk()

# create a menu attached to the top of the window
top = screen.winfo_toplevel()
menu_bar = Menu(top)
top["menu"] = menu_bar

# create the drop down and add items to it
drop_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=drop_menu)
drop_menu.add("command", label="New Game", command=reset)
drop_menu.add("command", label="Pause	 (p)", command=pause_game)
drop_menu.add("command", label="High Scores", command=show_scores)

# create sub-menu
sound_options = Menu(drop_menu, tearoff=0)
drop_menu.add_cascade(label="Options", menu=sound_options)
sound_options.add("command", label="toggle music", command=toggle_music)
sound_options.add("command", label="toggle sound effects", command=toggle_sounds)

# embed the game window within the tkinter one
game_window = Frame(screen, width=560, height=320)
game_window.pack(fill=BOTH, expand=YES)
game_id = game_window.winfo_id()

while True:

	#score = main.play_game()

	screen.mainloop()