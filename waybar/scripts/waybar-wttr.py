#!/usr/bin/env python

# Put your place like this:
# Country, city
place = 'YOUR_PLACE'


import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': '☀️',
    '116': '⛅',
    '119': '☁️',
    '122': '☁️',
    '143': '☁️',
    '176': '🌧️',
    '179': '🌧️',
    '182': '🌧️',
    '185': '🌧️',
    '200': '⛈️',
    '227': '🌨️',
    '230': '🌨️',
    '248': '☁️',
    '260': '☁️',
    '263': '🌧️',
    '266': '🌧️',
    '281': '🌧️',
    '284': '🌧️',
    '293': '🌧️',
    '296': '🌧️',
    '299': '🌧️',
    '302': '🌧️',
    '305': '🌧️',
    '308': '🌧️',
    '311': '🌧️',
    '314': '🌧️',
    '317': '🌧️',
    '320': '🌨️',
    '323': '🌨️',
    '326': '🌨️',
    '329': '❄️',
    '332': '❄️',
    '335': '❄️',
    '338': '❄️',
    '350': '🌧️',
    '353': '🌧️',
    '356': '🌧️',
    '359': '🌧️',
    '362': '🌧️',
    '365': '🌧️',
    '368': '🌧️',
    '371': '❄️',
    '374': '🌨️',
    '377': '🌨️',
    '386': '🌨️',
    '389': '🌨️',
    '392': '🌧️',
    '395': '❄️'
}

data = {}
weather = {}
if place == 'YOUR_PLACE':
    weather = requests.get("https://wttr.in/?format=j1").json()
else:
    weather = requests.get(f"https://wttr.in/{place}?format=j1").json()


def format_time(time):
    return time.replace("00", "").zfill(2)

def format_temp(temp):
    return (temp+"°").ljust(4)

def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }
    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

tempint = int(weather['current_condition'][0]['FeelsLikeC'])
extrachar = ''
if 0 < tempint < 10:
    extrachar = '+'

data['text'] = WEATHER_CODES[weather['current_condition'][0]['weatherCode']]+extrachar+weather['current_condition'][0]['FeelsLikeC']+"°C"

data['tooltip'] = f"{weather['nearest_area'][0]['country'][0]['value']}, {weather['nearest_area'][0]['areaName'][0]['value']}\n"
data['tooltip'] += f"{weather['current_condition'][0]['weatherDesc'][0]['value']} {WEATHER_CODES[weather['current_condition'][0]['weatherCode']]}, {weather['current_condition'][0]['temp_C']}°C\n"
data['tooltip'] += f"Wind 💨: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity 💧: {weather['current_condition'][0]['humidity']}%\n"

for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempC']}°C ⬇️ {day['mintempC']}°C "
    data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"

    for hour_index, hour in enumerate(day['hourly']):
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time']).strip()}h {WEATHER_CODES[hour['weatherCode']].strip()}, {format_temp(hour['FeelsLikeC']).strip()} {hour['weatherDesc'][0]['value'].strip()}, {format_chances(hour).strip()}"

        # Check if it's not the last hour of the day before adding a newline
        print(hour_index, len(day['hourly']))
        if i != 2 or hour_index < len(day['hourly']) - 1:
            data['tooltip'] += "\n"

print(json.dumps(data))
