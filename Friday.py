
'''
# beginner
1. Respond to "hello".
2. Provide predefined responses(mrng,evng,aftnn).
3. Time, date.
4. Searching the web for user queries.
'''

import pyttsx3
from datetime import datetime
import speech_recognition as sr

#---------------------------------------------------------------------------ENGINE INIT
engine = pyttsx3.init() #init the speech recognition engine
engine.setProperty("rate",180) #set the speech rate to 180 wpm

voices = engine.getProperty("voices")
# print(voices)
engine.setProperty("voice",voices[1].id)

#---------------------------------------------------------------------------SAYING THE TEXT(USER SPOKEN OR ENTERED)
def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

#---------------------------------------------------------------------------GREETING BASED ON TIME
def greetings():
    if greet >= 5 and greet < 12:
        talk("Good morning!, what can I do for you?")
    elif greet>=12 and greet<17:
        talk("Good Afternoon!, what can I do for you?")
    elif greet>=17 and greet<24:
        talk("Good Evening!, what can I do for you?")
    elif greet>=0 and greet<5:
        talk("You should go to sleep.. But, what can I do for you?")
# greetings()

#---------------------------------------------------------------------------SPEECH RECOGNISATION
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio)
        print("I think you said:- " + text)

    except sr.UnknownValueError:
        print("Sorry, I can't understand what you just said. Could you speak that again?")
        text = ""

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text = ""

    return text

time = datetime.now().time()
# print(time)
greet = time.hour
# listen()
date = datetime.now().date().strftime("%d/%m/%Y") #to change the date format
# print(date)

