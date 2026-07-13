import requests
import os

api_key = os.environ.get('OWM_API_KEY') #using environment variables to hide API Keys
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

location_rugby = { 'loc': 'rugby', 'lat': 52.373199,'lon': -1.261740} 

parameters = {
    'lat': 32.060255,
    'lon': 118.796877,
    'cnt': 4,
    'appid':api_key,
}

WillRain = False
message = ''

#make request to api using requesst module, 5 day weather forecast
response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
weather_data = response.json()
print(weather_data) #trying not to go over limit

#weather_data = {'cod': '200', 'message': 0, 'cnt': 4, 'list': [{'dt': 1783954800, 'main': {'temp': 299.27, 'feels_like': 299.27, 'temp_min': 298.21, 'temp_max': 299.27, 'pressure': 1022, 'sea_level': 1022, 'grnd_level': 1008, 'humidity': 51, 'temp_kf': 1.06, 'dew_point': 288.35}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 0}, 'wind': {'speed': 8.36, 'deg': 66, 'gust': 9.11}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2026-07-13 15:00:00'}, {'dt': 1783965600, 'main': {'temp': 298.31, 'feels_like': 298.24, 'temp_min': 296.39, 'temp_max': 298.31, 'pressure': 1022, 'sea_level': 1022, 'grnd_level': 1008, 'humidity': 52, 'temp_kf': 1.92, 'dew_point': 287.77}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 0}, 'wind': {'speed': 7.84, 'deg': 64, 'gust': 9.7}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2026-07-13 18:00:00'}, {'dt': 1783976400, 'main': {'temp': 293.6, 'feels_like': 293.48, 'temp_min': 290.76, 'temp_max': 293.6, 'pressure': 1023, 'sea_level': 1023, 'grnd_level': 1009, 'humidity': 68, 'temp_kf': 2.84, 'dew_point': 287.5}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 0}, 'wind': {'speed': 5.52, 'deg': 45, 'gust': 12.3}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2026-07-13 21:00:00'}, {'dt': 1783987200, 'main': {'temp': 287.93, 'feels_like': 287.94, 'temp_min': 287.93, 'temp_max': 287.93, 'pressure': 1023, 'sea_level': 1023, 'grnd_level': 1009, 'humidity': 95, 'temp_kf': 0, 'dew_point': 284.63}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 0}, 'wind': {'speed': 5.44, 'deg': 31, 'gust': 13.16}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2026-07-14 00:00:00'}], 'city': {'id': 2638978, 'name': 'Rugby', 'coord': {'lat': 52.3732, 'lon': -1.2617}, 'country': 'GB', 'population': 63323, 'timezone': 3600, 'sunrise': 1783915101, 'sunset': 1783974167}}

#check if it will rain in the next 12 hours
condition_codes = []

for i in range(0,4):
    id = weather_data['list'][0]['weather'][0]['id']
    condition_codes.append(id)

print(condition_codes)

for code in condition_codes:
    if code < 700:
        WillRain = True

if WillRain:
    message = 'Bring an Umbrella today because it will rain'
else:
    message = 'No rain forecasted today'

#use smtplib to send email if it will rain.

import smtplib

from_email = os.environ.get('MY_EMAIL')
password = os.environ.get('MY_PASSWORD')


connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()
connection.login(user=from_email, password=password)
connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=f'Subject:Rain Alert\n\n {message}')
connection.quit()
