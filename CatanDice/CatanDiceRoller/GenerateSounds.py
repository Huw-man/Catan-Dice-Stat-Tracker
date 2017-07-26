from gtts import gTTS
import os

for i in range(2,13):
    file_name = str(i)+".mp3" #
    tts= gTTS(text="you rolled a "+str(i), lang='en') #google text to speech
    tts.save("sounds\\"+file_name)

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# rel_path = "CatanDiceRoller\\sounds\\1.mp3"
# abs_file_path = os.path.join(script_dir, rel_path)
# print(abs_file_path)
os.system("sounds\\3.mp3")
