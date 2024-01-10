
'''
# beginner
1. Respond to "hello".
2. Provide predefined responses(mrng,evng,aftnn).
3. Time, date.
4. Searching the web for user queries.
'''
'''
#advanced
1. Advanced voice assistant with natural language processing capabilities. 
2. Sending emails
3. Setting reminders
4. Providing weather updates
5. Controlling smart home devices
6. Answering general knowledge questions
7. Integrating with third-party APIs for more functionality.
'''

import pyttsx3
from datetime import datetime
import speech_recognition as sr
import wikipedia as wiki
import smtplib
import openai
import requests
from dotenv import load_dotenv
import os
load_dotenv()


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

#---------------------------------------------------------------------------TAKING WRITTEN INPUT
def take_written_input(message):        #! Takes written input from user 
    talk(message)
    return input("Type your answer here ----> ").lower()

#---------------------------------------------------------------------------GREETING BASED ON TIME
def greetings(greet):
    if greet >= 5 and greet < 12:
        talk("Good morning!, what can I do for you?")
    elif greet>=12 and greet<17:
        talk("Good Afternoon!, what can I do for you?")
    elif greet>=17 and greet<24:
        talk("Good Evening!, what can I do for you?")
    elif greet>=0 and greet<5:
        talk("You should go to sleep.. But, what can I do for you?")

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

#---------------------------------------------------------------------------CHATGPT API
def generate_response(prompt):   
    #send the prompt to chatgpt and generate the reply
    message = prompt
    if message:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo"
        )
    return chat.choices[0].message.content
    # print(f"chatgpt: {reply}")
    
#--------------------------------------------------------------------------- SENDING EMAILS
def send_email(subject,receivers_email,body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'shahpreet2803@gmail.com' 
    sender_password = 'iefk jalo vkic gixg'  #app specific password used
    # subject = this.subject
    # receivers_email = "d36191973@gmail.com"  #dummy email address
    # body = "generated email"
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            msg = f'Subject: {subject}\n\n{body}'
            server.sendmail(sender_email, receivers_email, msg)
            print(f"Email sent to {receivers_email}")
    except Exception as e:
        print(f"Error sending email to {receivers_email}: {str(e)}")

#---------------------------------------------------------------------------WEATHER UPDATES
def weather_update(place):
    params = {
    'access_key': os.getenv('WEATHER_STACK_API'),
    'query': place
    }

    api_result = requests.get('https://api.weatherstack.com/current', params)

    api_response = api_result.json()

    talk(u'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature']))

#---------------------------------------------------------------------------VARIABLES FOR ANSWERING
time = datetime.now().time()
date = datetime.now().date().strftime("%d/%m/%Y") #to change the date format

#---------------------------------------------------------------------------RESPONSES ACCORDING TO QUERIES
greetings(time.hour)

while True:
    query = listen().lower()

    if "time" in query: #tell me the time
        text = time
        talk(text)

    if "date" in query: #tell me the date
        text = date
        talk(text)

    if "wikipedia" in query:  # tell me about Python from wikipedia
            query = query.replace("wikipedia", "")
            if "from" in query:
                query = query.replace("from", "")
            if "tell me" in query:
                query = query.replace("tell me", "")
            if "something" in query:
                query = query.replace("something", "")
            if "about" in query:
                query = query.replace("about", "")
            if "search" in query:
                query = query.replace("search","")
            # print("Query =", query)
            response = wiki.summary(query, sentences=2)
            talk(response)
    else:
        if "tell me" in query:
            query = query.replace("tell me", "")
        if "something" in query:
            query = query.replace("something", "")
        if "about" in query:
            query = query.replace("about", "")
        if "search" in query:
            query = query.replace("search","")
        talk(generate_response(query))

    if "email" in query:
        talk("Speak in the following format: ")
        talk("Speak subject: ")
        subject = listen()
        talk("Speak email of receiver: ")
        receivers_email = listen()
        talk(f"Did you say {receivers_email} ?")
        confirmation = listen()
        if confirmation != "ok" or confirmation != "yes":
            talk("Written input activated.. ")
            receivers_email = take_written_input("Type email of receiver: ")
        talk("Speak email body: ")
        body = listen()
        send_email(subject,receivers_email,body)

    if "weather" in query:
        if query.find("in")>0:   
            place = query.split("in")[1]
        elif query.find("for")>0:
            place = query.split("for")[1]
        elif query.find("of")>0:
            place = query.split("of")[1]
        elif query.find("at")>0:
            place = query.split("at")[1]
        elif query.find("'s")>0:
            place = query.split("'s")[0]
        weather_update(place)

    if "bye" in query or "goodbye" in query or "see you" in query:
        talk("Good bye..!!")
