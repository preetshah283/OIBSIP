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

openai.api_key = os.getenv('OPENAI_API_KEY')
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
def listen(timeout_duration=500, phrase_limit=10):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=timeout_duration, phrase_time_limit=phrase_limit)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""


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
    chat = None  # Initialize chat to None
    try:
        if not openai.api_key:
            raise ValueError("The OpenAI API key has not been set.")
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
    except Exception as e:
        print(f"An error occurred: {e}")

    if chat is not None:
        return chat.choices[0].message.content
    else:
        return "I'm sorry, I couldn't generate a response."
    
#--------------------------------------------------------------------------- SENDING EMAILS
def send_email(subject,receivers_email,body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.getenv('EMAIL') 
    sender_password = os.getenv('APP_SPECIFIC_PASSWORD')  #app specific password used

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

    try:
        api_result = requests.get('https://api.weatherstack.com/current', params)
        if api_result.status_code == 200:
            api_response = api_result.json()
            if 'current' in api_response and 'temperature' in api_response['current']:
                temperature = api_response['current']['temperature']
                location_name = api_response['location']['name']
                talk("Current temperature in {} is {}℃".format(location_name, temperature))
            else:
                talk("I'm sorry, I couldn't fetch the weather for you. Please try again later.")
        else:
            talk("I'm sorry, there was a problem retrieving the weather information.")
    except requests.RequestException as e:
        talk("I'm sorry, I couldn't fetch the weather due to a network problem.")

#---------------------------------------------------------------------------VARIABLES FOR ANSWERING
time = datetime.now().time()
date = datetime.now().date().strftime("%d/%m/%Y") #to change the date format

#---------------------------------------------------------------------------RESPONSES ACCORDING TO QUERIES
greetings(time.hour)

while True:
    current_time = datetime.now().time().strftime("%I:%M %p")
    current_date = datetime.now().date().strftime("%d/%m/%Y")
    query = listen().lower()

    if not query:  # If the query is empty, skip this iteration
        continue

    if "time" in query:
        talk(current_time)

    if "date" in query:
        talk(current_date)

    if "wikipedia" in query:  # tell me about Python from wikipedia
        # Process the query to remove unnecessary words
        for word in ["wikipedia", "from", "tell me", "something", "about", "search"]:
            query = query.replace(word, "")
        try:
            response = wiki.summary(query, sentences=2)
            talk(response)
        except wiki.exceptions.DisambiguationError as e:
            talk("There are multiple entries for this term. Please be more specific.")
        except wiki.exceptions.PageError:
            talk("I couldn't find any information on that topic.")
    else:
        # For other queries, call generate_response
        response = generate_response(query)
        talk(response)

    if "email" in query:
        talk("Speak in the following format: ")
        talk("Speak subject: ")
        subject = listen()
        talk("Speak email of receiver: ")
        receivers_email = listen()
        talk(f"Did you say {receivers_email} ? Please reply as yes or no.")
        confirmation = listen()
        if "ok" in confirmation or "yes" in confirmation:
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

    elif "bye" in query or "goodbye" in query or "see you" in query:
        talk("Good bye..!!")
        exit(0)
        