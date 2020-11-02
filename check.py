import datetime
import hashlib
import requests
import getpass
import json
import sys

if len(sys.argv) == 3:
	login		= str(sys.argv[1])
	password	= str(sys.argv[2])
else:
	login		= str(input("Введите логин: "))
	password	= str(getpass.getpass("Введите пароль: "))

current_date_utc= datetime.datetime.utcnow().strftime("%Y.%m.%d_%H:%M:%S")
input_value		= login+current_date_utc+password
calculate_hash	= str(hashlib.sha256(input_value.encode()).hexdigest())
params = (
    ('user_login', login),
    ('hash_sum', calculate_hash)
)
response = requests.get('http://127.0.0.1:8000/metrics', params=params)
print(json.loads(response.content.decode()))