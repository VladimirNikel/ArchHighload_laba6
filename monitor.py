from check import collection_metrics
import getpass
import datetime

login		= str(input("1Введите логин: "))
password	= str(getpass.getpass("1Введите пароль: "))

pull_serv=["127.0.0.1:8000","194.61.2.84:5020", "194.61.2.84:5030"]

for i in range(len(pull_serv)):
	print("я потопал в ",pull_serv[i])
	print(collection_metrics(pull_serv[i], login, password))




