
'''
# beginner
1. Respond to "hello".
2. Provide predefined responses(mrng,evng,aftnn).
3. Time, date.
4. Searching the web for user queries.
'''

import pyttsx3
from datetime import datetime


engine = pyttsx3.init() #init the speech recognition engine
engine.setProperty("rate",180) #set the speech rate to 180 wpm

voices = engine.getProperty("voices")
# print(voices)

engine.setProperty("voice",voices[1].id)

time = datetime.now().time()
# print(time)

greet = time.hour
def talk(text):
    text = text + ", What can I do for you?"
    engine.say(text)
    engine.runAndWait()
    print(text)

def greetings():
    if greet >= 5 and greet < 12:
        talk("Good morning!")
    elif greet>=12 and greet<17:
        talk("Good Afternoon!")
    elif greet>=17 and greet<24:
        talk("Good Evening!")
    elif greet>=0 and greet<5:
        talk("You should go to sleep.. But")

greetings()

date = datetime.now().date().strftime("%d/%m/%Y") #to change the date format
# print(date)
