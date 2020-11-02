from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

import uvicorn

import check_auth_data		#подключили наш проверяющий файлик
import time
#import datetime

#необходимо, чтобы работать с json'ом
import json

#необходимо для работы с переменными окружения
import os
import sys

#необходимо для работы с API openweathermap
import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

config_dict = get_default_config()
config_dict['language'] = 'ru'

#тут находится ключ с сайта OpenWeatherMap
app_key = os.environ.get('OWM_APP_KEY')
owm = pyowm.OWM(app_key, config_dict)

my_id = sys.argv[1]

programMetrics=[0,0,0]
#0 - количество посещений корневого сайта ("/")
#1 - количество отображения текущей погоды в указанном городе ("/v1/current/")
#2 - обращений к сайту OpenWeatherMap

processing_time_of_the_request_root_page = [] 			#время обработки запроса корневой страницы
processing_time_of_the_request_current_weather = []		#время обработки запроса текущей погоды
processing_time_of_the_request_forecast_weather = []	#время обработки запроса прогноза погоды

def calculate_average_value():
	global processing_time_of_the_request_root_page
	global processing_time_of_the_request_current_weather
	global processing_time_of_the_request_forecast_weather
	average1 = float(0)
	average2 = float(0)
	average3 = float(0)

	try:
		n = 0
		for i in processing_time_of_the_request_root_page:
			average1 += processing_time_of_the_request_root_page.pop()
			n+=1
		average1 /= n
	except ZeroDivisionError:
		average1 = float(0)

	try:
		n = 0
		for i in processing_time_of_the_request_current_weather:
			average2 += processing_time_of_the_request_current_weather.pop()
			n+=1
		average2 /= n
	except ZeroDivisionError:
		average2 = float(0)
	
	try:
		n = 0	
		for i in processing_time_of_the_request_forecast_weather:
			average3 += processing_time_of_the_request_forecast_weather.pop()
			n+=1
		average3 /= n
	except ZeroDivisionError:
		average3 = float(0)
	
	return json.dumps({"root_page":average1,"current":average2,"forecast":average3})




@app.get("/")
def print_web():
	time_to_start = time.time()
	global programMetrics
	global processing_time_of_the_request_root_page
	programMetrics[0]+=1
	html_content = """<html>
	<head>
	<title>Погодный сервис</title>
	<style>
		button.knopka {
		color: #fff; 
		background: #FFA500; 
		padding: 5px; 
		border-radius: 5px;
		border: 2px solid #FF8247;
		} 
		button.knopka:hover { 
		background: #FF6347; 
		}
	</style>
	</head>
	<body>
		<h1>Погодный сервис от Nikel</h1>
		<table>
		<tr>
			<td>
				<p>Узнать текущую погоду</p>
				<form action="/v1/current/" method="GET" name="form1">
					<input name="city" type="text" />
					<button class="knopka">Перейти сюда</button>
				</form>
			</td>
		</tr>
		<tr>
			<td>
				<p>Узнать прогноз погоды</p>
				<form action="/v1/forecast/" method="GET" name="form2">
					<input name="city" type="text" />
					<select name="timestamp">
						<option>Выберите из списка</option>
						<option>1h</option>
						<option>3h</option>
						<option>tomorrow</option>
						<option>yesterday</option>
					</select>
					<button class="knopka">Перейти сюда</button>
				</form>
			</td>
		</tr>
		</table>
	</body>
</html>
"""
	processing_time_of_the_request_root_page.append(time.time() - time_to_start)
	return HTMLResponse(content=html_content, status_code=200)

@app.get("/metrics")
def metrics(user_login: str, hash_sum: str):
	global programMetrics
	result_json = json.loads(check_auth_data.check_value_hash(user_login, hash_sum))
	if (result_json["result"]=='true'):
		count_visit_site_root 					= programMetrics[0]#0 - количество посещений корневого сайта ("/")
		count_dispays_current_weather_in_city 	= programMetrics[1]#1 - количество отображения текущей погоды в указанном городе ("/v1/current/")
		count_requests_to_OpenWeatherMap		= programMetrics[2]#2 - обращений к сайту OpenWeatherMap
		programMetrics=[0,0,0]
		return json.dumps({"status_auth":"ok", "id_service": my_id, "count_visit_root": count_visit_site_root, "count_dispays_current_weather": count_dispays_current_weather_in_city, "count_requests_to_OWM": count_requests_to_OpenWeatherMap, "avr": json.loads(calculate_average_value()) })
	else:
		return json.dumps({"status_auth":"invalid login or password", "id_service": my_id})

@app.get("/v1/current/")
#city=<name city>
#http://127.0.0.1:8000/v1/current/?city=Moscow
def current(city: str):
	time_to_start = time.time()
	global programMetrics
	global processing_time_of_the_request_current_weather
	programMetrics[1]+=1
	programMetrics[2]+=1
	mgr = owm.weather_manager()

	observation = mgr.weather_at_place(city)
	w = observation.weather
	temp = w.temperature('celsius')['temp']
	#вывод в консоль
	print(" request: " + city + "\t" + w.detailed_status + "\t" + str( temp ))
	processing_time_of_the_request_current_weather.append(time.time() - time_to_start)
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp, "id_service": my_id})


@app.get("/v1/forecast/")
#city=<name city>&timestamp=<timestamp>
#http://127.0.0.1:8000/v1/forecast/?city=Moscow&timestamp=3h
def forecast(city: str, timestamp: str):
	time_to_start = time.time()
	global programMetrics
	global processing_time_of_the_request_forecast_weather
	programMetrics[2]+=1
	mgr = owm.weather_manager()

	observation = mgr.forecast_at_place(city, "3h") #данной командой стягивается прогноз погоды на ближайшие 5 дней с частотой 3 часа
	if timestamp == "1h":
		timest = timestamps.next_hour()
	elif timestamp == "3h":
		timest = timestamps.next_three_hours() 
	elif timestamp == "tomorrow":
		timest = timestamps.tomorrow()
	elif timestamp == "yesterday":
		timest = timestamps.yesterday()
	else:
		timest = timestamps.now();
	w = observation.get_weather_at(timest)
	temp = w.temperature('celsius')['temp']
	#вывод в консоль
	print(" request: " + city + "\ttime: "+ str(timest) + "\t" + w.detailed_status + "\t" + str( temp ))
	processing_time_of_the_request_forecast_weather.append(time.time() - time_to_start)
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp, "id_service": my_id})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)