import requests
from tkinter import *
import os
from dotenv import load_dotenv

load_dotenv()
def get_weather(city):
    api_key = os.getenv('OPEN_WEATHER_MAP_API')
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&rootid={api_key}&units=metric"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error Connecting: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def display_weather(weather_data):
    if weather_data:
        name = weather_data.get('name', 'Unknown Location')
        desc = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        final_info = f"{name}\n{desc}"
        final_data = f"Temperature: {temp}°C\nHumidity: {humidity}%"
    else:
        final_info = "Error retrieving weather data"
        final_data = "Please check the city name or your network connection."

    infolabel.config(text=final_info)
    datalabel.config(text=final_data)

def search():
    city = city_text.get()
    weather = get_weather(city)
    display_weather(weather)

root = Tk()
root.geometry("700x400")
root.title("Weather Check")

city_text = StringVar()
city_entry = Entry(root, textvariable = city_text).pack()

search_button = Button(root, text = "Search Weather", command = search).pack()

infolabel = Label(root, font = ("comicsansms 15 italics")).pack()

datalabel = Label(root, font = ("comicsansms 15")).pack()

root.mainloop()