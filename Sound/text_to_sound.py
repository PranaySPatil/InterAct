# Import the required module for text 
# to speech conversion
from gtts import gTTS
#from vlc import MediaPlayer as mp
 
# This module is imported so that we can 
# play the converted audio
import os
 
# The text that you want to convert to audio
#mytext = 'Hey Dude'
 
# Language in which you want to convert
language = 'en'
 
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
l=['Baby', 'Bag', 'Car', 'Cat', 'Christmas', 'Hello', 'Humid', 'Hungry', 'I Love you', 'Monkey', 'Please', 'Thank You']
for mytext in l:
	myobj = gTTS(text=mytext, lang=language, slow=False)
 
# Saving the converted audio in a mp3 file named
# welcome 
	myobj.save(mytext+".mp3")
 
# Playing the converted file
#os.system("mpg123.exe welcome.mp3")
#p = mp("welcome.mp3")
#p.play()