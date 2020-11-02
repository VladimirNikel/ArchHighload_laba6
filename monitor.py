from check import collection_metrics
import getpass
import datetime
import threading
import json

login		= str(input("Введите логин: "))
password	= str(getpass.getpass("Введите пароль: "))
time_to_wait= int(input("Введите количество секунд, через которое будут опрашиваться сервера: "))
if time_to_wait < 1:
	time_to_wait=60
	print("Вы ввели некорректное значение. Выставлены стандартные настройки: опрос серверов будет происходить каждые 60 секунд.")

pull_serv=["127.0.0.1:8000", "194.61.2.84:5020", "194.61.2.84:5030"]
print("Начал работать в", datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"))

def main_job():
	for i in range(len(pull_serv)):
		print(json.loads(collection_metrics(pull_serv[i], login, password)))

try:
	while 1:
		print("Данные на", datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"))
		t = threading.Timer(time_to_wait, main_job)
		t.start()
		t.join()

except KeyboardInterrupt:
	print("\n\nЧто ж, до встречи...\nОсталось долждаться ответа от количества потоков: ",threading.active_count()-1)
	exit(0)
