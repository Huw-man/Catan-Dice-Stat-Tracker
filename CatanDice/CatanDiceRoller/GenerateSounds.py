from gtts import gTTS
import os

for i in range(2,13):
    for p in ('red', 'white', 'blue', 'orange', 'green', 'brown'):
        file_name = p+str(i)+".mp3"
        print("generating "+file_name)
        tts= gTTS(text= p+" rolled a, "+str(i), lang='en', slow=False) #google text to speech
        tts.save("sounds\\"+file_name)
