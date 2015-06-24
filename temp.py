import os

# an initial set of high scores that can be used to pre-populate the scoreboard
highscores = []
key = 30
for i in range(5):
	highscores.append((key, "abba"))
	key -= 5
	
file = open(os.path.join('data', 'highscores.txt'), 'w')
file.write(repr(highscores))
file.close()