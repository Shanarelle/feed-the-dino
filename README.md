# feed-the-dino
A space invader style game where you control a purple triceratops and have to feed it orange candy.

Mp3 music provided by http://www.bensound.com

In order to run the game you will need python 2.7 with pygame installed.
If you download the files you can run the game using 
        python main.py
from a terminal window in the rainingCandy directory, which should open a window where the game will execute.

Feel free to delete the highscores.txt so that you can track your own scores.


You can also try running nommin.py and see what happens

#######################################################
TROUBLESHOOTING

if there is no background music and you are playing on a mac then try running these three commands
(omit the first one if you already have brew installed)

1.	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2.	brew install libvorbis
3.	brew reinstall sdl_mixer
